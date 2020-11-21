"""
###############################
@author: zhenwei.shi, Maastro##
###############################

This scrip shows how to generate itk objects (nrrd, etc) from DICOM Segmentation objects
Before running this script, you need to add dcmqi tool to your system path by

-- windows: "export PATH="$(pwd)/dcmqi/bin":$PATH"
-- Linux: "export PATH="$(pwd)/dcmqi_linux/bin":$PATH"

"""
from __future__ import print_function

import os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import glob
import shutil
from DicomDatabase import DicomDatabase
import numpy as np
import re
import numpy as np
from subprocess import call

def get_lungslice(ptid,roi,Image,Mask,output_dir):
    print(''*30)
    print('Starting to get lung slice')
    #convert image to array
    mask_array = sitk.GetArrayFromImage(Mask)
    image_array  = sitk.GetArrayFromImage(Image)
    ind_list = [] 
    #detect the index of slices including tomour
    for i in range(mask_array.shape[0]):
        if np.sum(mask_array[i,:,:]):
            ind_list.append(i)
    for j in ind_list:
        single_image = image_array[j,:,:]
        single_mask = mask_array[j,:,:]
        # export image name patient id + ROI + slice index j
        fig_name_im = ptid + '_' + roi +'_' + 'slice'+ str(mask_array.shape[0]-j)
        fig_name_mask = ptid + '_' + roi +'_' + 'slice'+ str(mask_array.shape[0]-j)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
#         np.save('./output/LCTSeg/image/' + fig_name_im,single_image)
#         np.save('./output/LCTSeg/mask/' + fig_name_mask,single_mask)
        plt.imsave((output_dir + 'image/'+ fig_name_im + '.png'),single_image,cmap = 'gray')
        plt.imsave((output_dir + 'mask/' + fig_name_mask + '.png'),single_mask,cmap = 'gray')
    print('All DL input image of patient %s have been done !!!' % ptid)

# binary package: convert nrrd to SEG.dcm using dcmqi
def DCMRT2SEG(inputlabelList,inputDICOMDirectory,inputMetadata,outputSEGfile,outputDir):
    outputDICOM = os.path.join(outputDir,outputSEGfile)
    try:
        call(['itkimage2segimage', '--inputImageList', inputlabelList,'--inputDICOMDirectory',inputDICOMDirectory,\
              '--inputMetadata',inputMetadata, '--outputDICOM', outputDICOM])
    except:
        print('Error: failed to pack dcm image to SEG.dcm')

# convert SEG objects to ITK nrrd images
def SEG2ITKimage(inputSEGfile, segmentsDir,outputfile):
    if not os.path.exists(segmentsDir):
        os.mkdir(segmentsDir)    
    try:
        call(['segimage2itkimage', '--inputDICOM', inputSEGfile, '--outputDirectory', segmentsDir,'-p', outputfile])
    except:
        print('Error: Failed to pack SEG to nrrd image')

#-------------------------USER parameters-------------------------
if __name__ == "__main__":

    output_dir = '../output/'
    segmentsDir = output_dir + 'ITKimage_mask/'
    SEG_dir = '../output/DCMSEG'
    # -----------------------------------------------------------
    filesnames = os.listdir(SEG_dir)
    for file in filesnames:
        outputfile = file[0:-4]
        inputSEGfile = os.path.join(SEG_dir,file)
        SEG2ITKimage(inputSEGfile, segmentsDir,outputfile)
