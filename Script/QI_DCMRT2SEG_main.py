"""
###############################
@author: zhenwei.shi, Maastro##
###############################

This scrip shows that how to generate ITK object (nrrd,etc) of specific ROI from DICOM-RT using platimatch, 
then generate DICOM Segmentation objects
Before running this script, you need to add dcmqi tool to your system path by

Implement the following code, first go to directory /ARGOS/
-- windows: add dcmqi/bin path to enviroment variable
-- Linux: "export PATH="$(pwd)/dcmqi_linux/bin":$PATH" 

"""
from __future__ import print_function

import os
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import glob
import shutil
from DicomDatabase import DicomDatabase
import numpy as np
from subprocess import call
import QI_metadata_generator as mg


#-------------------------USER-------------------------------
walk_dir = '../Data/'                                   # specify data directory
tmp_dir  = '../output/Tmp_ITKimage/'                    # specify tempral ITK image directory
output_dir = '../output/DCMSEG/'                        # specify output directory
ITK_CT_dir  = '../output/ITKimage_CT/'                  # specify ITKimage CT directory
outputdir= '../output/metadata/'
output_mask = '../output/ITKimage_mask'

# ----------------------Functions ---------------------------
# # convert nrrd to SEG.dcm using dcmqi
def DCMRT2SEG(inputlabelList,inputDICOMDirectory,inputMetadata,outputSEGfile,outputDir):
    outputDICOM = os.path.join(outputDir,outputSEGfile)
    try:
        call(['itkimage2segimage', '--inputImageList', inputlabelList,'--inputDICOMDirectory',inputDICOMDirectory,\
              '--inputMetadata',inputMetadata, '--outputDICOM', outputDICOM])
    except:
        print('Error: failed to pack dcm image to SEG.dcm')

# convert SEG objects to ITK nrrd images
def SEG2ITKimage(inputSEGfile, segmentsDir,ptid):
    if not os.path.exists(segmentsDir):
        os.mkdir(segmentsDir)    
    try:
        call(['segimage2itkimage', '--inputDICOM', inputSEGfile, '--outputDirectory', segmentsDir,'-p', ptid])
    except:
        print('Error: Failed to pack SEG to nrrd image')

# convert DICOM specified ROIs in the RTSTRUCT file to ITK image using plastimatch
def DCMRT2NRRD(inputRtDir,inputImageDir,exportDir):
    try:
        call(['plastimatch', 'convert','--input',inputRtDir,'--output-prefix',exportDir, '--prefix-format', 'nrrd',\
        '--referenced-ct',inputImageDir])
    except:
        print("Error: plastimatch failed to convert RT to mask.nrrd")


# convert DICOM image to TIK image using plastimatch
def DCMImage2NRRD(inputImageDir,ptid,exportDir):
    image = os.path.join(exportDir,ptid + '_image.nrrd')
    try:
        call(['plastimatch', 'convert','--input',inputImageDir,'--output-img',image])
    except:
        print("Error: plastimatch failed to convert image to image.nrrd")
    return image

#-----------------create temporal CT/STRUCT directories-----------
CTWorkingDir = "../CTFolder"
STRUCTWorkingDir = "../StructFolder"
if not os.path.exists(CTWorkingDir):
  os.makedirs(CTWorkingDir)
if not os.path.exists(STRUCTWorkingDir):
  os.makedirs(STRUCTWorkingDir)
# -----------------------------------------------------------
# initialize dicom DB
dicomDb = DicomDatabase()
# walk over all files in folder, and index in the database
dicomDb.parseFolder(walk_dir)
# -----------------------------------------------------------
excludeStructRegex = "(Patient.*|BODY.*|Body.*|NS.*|Couch.*)"
if os.environ.get("EXCLUDE_STRUCTURE_REGEX") is not None:
    excludeStructRegex = os.environ.get("EXCLUDE_STRUCTURE_REGEX")
# -----------------------------------------------------------
# generate json file
mg.generator(walk_dir,outputdir)
# -----------------------------------------------------------
# loop over patients
for ptid in dicomDb.getPatientIds():
    print("staring with Patient %s" % (ptid))
    print(ptid)
    # get patient by ID
    myPatient = dicomDb.getPatient(ptid)
    # loop over RTStructs of this patient
    for myStructUID in myPatient.getRTStructs():
        print("Starting with RTStruct %s" % myStructUID)
        # Get RTSTRUCT by SOP Instance UID
        myStruct = myPatient.getRTStruct(myStructUID)
        # Get CT which is referenced by this RTStruct, and is linked to the same patient
        # mind that this can be None, as only a struct, without corresponding CT scan is found
        myCT = myPatient.getCTForRTStruct(myStruct)
        # check if the temperal CT/STRUCT folder is empty
        if not (os.listdir(CTWorkingDir)==[] and os.listdir(STRUCTWorkingDir)==[]):
            ct_files = glob.glob(os.path.join(CTWorkingDir,'*'))
            for f in ct_files:
                os.remove(f)
            struct_files = glob.glob(os.path.join(STRUCTWorkingDir,'*'))
            for f in struct_files:
                os.remove(f)        
        # only show if we have both RTStruct and CT
        if myCT is not None:
            # copy RTSTRUCT file to tmp folder as 'struct.dcm'
            shutil.copy2(myStruct.getFileLocation(),os.path.join(STRUCTWorkingDir,'struct.dcm'))
            # copy DICOM slices to tmp folder as 'struct.dcm'
            slices = myCT.getSlices()
            for i in range(len(slices)):
                shutil.copy2(slices[i],os.path.join(CTWorkingDir,str(i)+".dcm"))   

            #-------------------------USER-------------------------------
            # Generate binary mask
            print('---'*10)
            print('Generate binary mask of %s' %ptid)
            print('---'*10)
            inputImageDir = CTWorkingDir
            inputRtDir = STRUCTWorkingDir

            os.makedirs(os.path.join(tmp_dir,ptid))
            exportDir = os.path.join(tmp_dir,ptid)
            # Convert ROI to ITK image volume
            DCMRT2NRRD(inputRtDir,inputImageDir,exportDir)
            # Convert DICOM image to ITK image volume
            DCMImage2NRRD(inputImageDir,ptid,ITK_CT_dir)
            # -------------------------USER-------------------------------
            # Generate DICOM-SEG
            print('---'*10)
            print('Generate DCIOM-SEG of %s' %ptid)
            print('---'*10)

            tmp_mask_dir = os.path.join(tmp_dir,ptid)                          
            inputSEG = ptid + '_' + 'SEG.dcm'
            
            mask_list = glob.glob(os.path.join(tmp_mask_dir,'*.nrrd'))
            mask_list.sort()     
            inputlabelList = ','.join(map(str,mask_list))

            # generate metadata json file per patient
            Jsonfile = '../output/metadata/' + ptid +'.json'
            # Generate DICOM SEG
            DCMRT2SEG(inputlabelList,inputImageDir,Jsonfile,inputSEG,output_dir)