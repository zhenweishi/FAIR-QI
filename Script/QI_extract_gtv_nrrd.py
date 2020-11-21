import os
import pydicom as dicom
import json
import shutil

homeFolder='../Data/Lung1'
ITKimage_folder = '../output/ITKimage_mask/'
listOfJsonFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(ITKimage_folder) for f in filenames if f.endswith('json')]
listOfDcmFiles  = [os.path.join(dp, f) for dp, dn, filenames in os.walk(homeFolder) for f in filenames if f.endswith('dcm')]

def get_patient_name(list_of_dcm_files):
    patient_name1 = []
    for ff in list_of_dcm_files:
        try:
            this = dicom.read_file(ff, force=True)
            patient_name1.append(this.PatientID)
        except:
            pass
    
    patient_name = []
    for i in patient_name1:
        if i not in patient_name:
            patient_name.append(i)
    
    return patient_name
 

patid = get_patient_name(listOfDcmFiles)
total = []
number_of_gtv = []

# find GTV mask
for i in range(0,len(patid)):
    f = open(ITKimage_folder+str(patid[i]+'_SEG-meta.json'), encoding='utf-8')
    dictt = json.load(f)
    number_of_attributes = len(dictt["segmentAttributes"])
    #print(number_of_attributes,'--------------------')
    result = []
    for j in range(0,number_of_attributes):
        #print(dictt["segmentAttributes"][j][0]["SegmentedPropertyTypeCodeSequence"]["CodeValue"])
        if dictt["segmentAttributes"][j][0]["SegmentedPropertyTypeCodeSequence"]["CodeValue"] == "86049000":
            result.append(dictt["segmentAttributes"][j][0]["labelID"])

    total.append(result)

# count number of GTV mask   
for k in range(0, len(total)):
    number_of_gtv.append(len(total[k]))

# rename mask
try:
    for i in range(0,len(patid)):
        f = open(ITKimage_folder+str(patid[i]+'_SEG-meta.json'), encoding='utf-8')
        dictt = json.load(f)
        number_of_attributes = len(dictt["segmentAttributes"])
        print(patid[i])
        for j in range(0,number_of_attributes):
            roi = dictt["segmentAttributes"][j][0]["SegmentDescription"]
            os.rename(ITKimage_folder+patid[i]+'_SEG-'+str(j+1)+'.nrrd', ITKimage_folder+patid[i]+'_SEG_'+roi+'.nrrd')
except:
    pass
                  


# create folder
for j in range(0,len(number_of_gtv)):
    folder_name = ITKimage_folder+patid[j]+'_GTV_mask'
    try:
        os.mkdir(folder_name)
    except:
        pass


# move GTV mask to specific folder
for j in range(0,len(number_of_gtv)):
    folder_name = ITKimage_folder+patid[j]+'_GTV_mask/'
    for k in range(0,(number_of_gtv[j])):
        print(ITKimage_folder+patid[j]+'_SEG_GTV-'+''+str(k+1)+'.nrrd')
        shutil.move(ITKimage_folder+patid[j]+'_SEG_GTV-'+str(k+1)+'.nrrd',folder_name)
    

