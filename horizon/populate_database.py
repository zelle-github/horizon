# encoding=utf8
import os, sys, glob
import fnmatch

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horizon.settings")
django.setup()

#from django.conf import settings
#from django.db import models
import SimpleITK as sitk

from django.utils import timezone
from django.db import connection
from databrowser.models import Dataset, Patient, Study, Image, Segmentation
       
def main():
    #datasetpath = sys.argv[1]
    dataset_rootpath = "C:\\Users\\Vivek Narayan\\Desktop\\Horizon\\www\\media\\datasets\\TCGA-GBM"
    dataset_description = "Test GBM dataset from TCGA"
    dataset = loadDataset(dataset_rootpath, description=dataset_description)
    
    loadPatients(dataset)
    dataset_patients = Patient.objects.filter(fk_patient_dataset=dataset) 
    
    for patient in dataset_patients:
        loadStudies(patient)
        patient_studies = Study.objects.filter(fk_study_patient=patient)
        
        for study in patient_studies:
            loadImages(study)
            study_images = Image.objects.filter(fk_image_study=study)
    
            loadSegmentations(study, study_images)
         
def loadDataset(dataset_rootpath, start_date=None, description=None):
    dataset_name = str(os.path.basename(dataset_rootpath))
    if start_date is None: start_date = timezone.now()
    if description is None: description = "No Description"
    
    if dataset_name not in [dataset.dataset_name for dataset in Dataset.objects.all()]:
        new_dataset = Dataset(dataset_name = dataset_name, 
                      dataset_rootpath = str(dataset_rootpath),
                      dataset_startdate = start_date,
                      dataset_description = description)
        new_dataset.save()
    else:
        new_dataset = Dataset.objects.get(dataset_name=dataset_name)       
    return new_dataset

    
def loadPatients(dataset):
    dataset_path = str(dataset.dataset_rootpath)
    patient_subdirs = [subdir for subdir in glob.glob(os.path.join(dataset_path,'*')) if os.path.isdir(subdir)]
    
    try:
        dataset_patients = [patient.patient_dicomid for patient in Patient.objects.filter(fk_patient_dataset=dataset)]
    except Patient.DoesNotExist:
        dataset_patients = []
        
    for patient_subdir in patient_subdirs:
        new_patient_dicomid = os.path.basename(patient_subdir)
        if new_patient_dicomid not in dataset_patients:
            new_patient = Patient(fk_patient_dataset = dataset,
                                  patient_rootpath = str(patient_subdir),
                                  patient_dicomid = new_patient_dicomid)
            new_patient.save()

def loadStudies(patient):
    patient_path = str(patient.patient_rootpath)
    study_subdirs = [subdir for subdir in glob.glob(os.path.join(patient_path,'*')) if os.path.isdir(subdir)]
    
    try:
        patient_studies = [study.study_name for study in Study.objects.filter(fk_study_patient=patient)]
    except Study.models.DoesNotExist:
        patient_studies = []
        
    for study_subdir in study_subdirs:
        new_study_name = os.path.basename(study_subdir)
        if new_study_name not in patient_studies:
            new_study = Study(fk_study_patient = patient,
                              study_rootpath = str(study_subdir),
                              study_name = new_study_name)
            new_study.save()

def loadImages(study):
    study_path = str(study.study_rootpath)
    study_subdirs = [subdir for subdir in glob.glob(os.path.join(study_path,'*')) if os.path.isdir(subdir)]
    
    reconstructions_dir = [subdir for subdir in study_subdirs if 'reconstructions' in os.path.basename(subdir).lower()][0]
    
    image_filepaths = []
    for r,d,f in os.walk(reconstructions_dir):
        [image_filepaths.append(str(os.path.join(r,file))) for file in fnmatch.filter(f,'*.nrrd')]
    
    try:
        study_images = [image.image_filepath for image in Image.objects.filter(fk_image_study = study)]
    except Image.models.DoesNotExist:
        study_images = []
        
    for image_filepath in image_filepaths:
        if image_filepath not in study_images: 
            nrrd_dict = nrrdReader(image_filepath)
            new_image = Image(fk_image_study = study,           
                              image_filepath = image_filepath,
                              image_name = str(os.path.splitext(os.path.basename(image_filepath))[0]),
                              image_spaceorigin = nrrd_dict['space origin'],
                              image_endian = nrrd_dict['endian'],
                              image_spacedirections = nrrd_dict['space directions'],
                              image_space = nrrd_dict['space'],
                              image_sizes = nrrd_dict['sizes'],
                              image_encoding = nrrd_dict['encoding'],
                              image_nrrdname = nrrd_dict['nrrdname'],
                              image_kinds = nrrd_dict['kinds'],
                              image_type = nrrd_dict['type'],
                              image_dimension = nrrd_dict['dimension'])    
            new_image.save()
            
def loadSegmentations(study, study_images):
    study_path = str(study.study_rootpath)
    study_subdirs = [subdir for subdir in glob.glob(os.path.join(study_path,'*')) if os.path.isdir(subdir)]
    
    segmentations_dir = [subdir for subdir in study_subdirs if 'segmentations' in os.path.basename(subdir).lower()][0]
    
    segmentation_filepaths = []
    for r,d,f in os.walk(segmentations_dir):
        [segmentation_filepaths.append(str(os.path.join(r,file))) for file in fnmatch.filter(f,'*.nrrd')]
    
    #pdb.set_trace()
    for study_image in study_images:
        for segmentation_filepath in segmentation_filepaths:
            if str(study_image.image_name.lower()) in str(os.path.basename(segmentation_filepath).lower()):
                try:
                    segmentation_images = [segmentation.segmentation_filepath for segmentation in Segmentation.objects.filter(fk_segmentation_image = study_image)]
                except Segmentation.DoesNotExist:
                    segmentation_images = []
                if segmentation_filepath not in segmentation_images: 
                    nrrd_dict = nrrdReader(segmentation_filepath)
                    new_segmentation = Segmentation(fk_segmentation_image = study_image,           
                                                    segmentation_filepath = segmentation_filepath,
                                                    segmentation_name = str(os.path.splitext(os.path.basename(segmentation_filepath))[0]),
                                                    segmentation_spaceorigin = nrrd_dict['space origin'],
                                                    segmentation_endian = nrrd_dict['endian'],
                                                    segmentation_spacedirections = nrrd_dict['space directions'],
                                                    segmentation_space = nrrd_dict['space'],
                                                    segmentation_sizes = nrrd_dict['sizes'],
                                                    segmentation_encoding = nrrd_dict['encoding'],
                                                    segmentation_nrrdname = nrrd_dict['nrrdname'],
                                                    segmentation_kinds = nrrd_dict['kinds'],
                                                    segmentation_type = nrrd_dict['type'],
                                                    segmentation_dimension = nrrd_dict['dimension'])
                    new_segmentation.save()
                 
def nrrdReader(nrrdfilepath):
    nrrdpath = nrrdfilepath
    
    nrrdheaderlist = []
    with open(nrrdpath, 'r') as nrrdfile:
        fileparse = (line for line in nrrdfile)
        while True:
            try:  
                currline = next(fileparse)
                currline.decode('ascii')
            except UnicodeDecodeError:
                break
            else:
                nrrdheaderlist.append(str(currline))
          
    headers = ['nrrdname','type','dimension','space','sizes','space directions','kinds','endian','encoding','space origin']
    nrrdheaderdict = {k:'Unknown' for k in headers}
    nrrdheaderdict['nrrdname'] = str(nrrdheaderlist[0].strip())
    for item in nrrdheaderlist:
        if '#' in item:
            continue
        field = item.split(':')[0] 
        if field in headers:
            fieldvalue = str(item.split(':')[1].strip())
            if fieldvalue is not None and fieldvalue != '':
                nrrdheaderdict[field] = fieldvalue
                
    return nrrdheaderdict    
        
def nrrdconverter():
    image_filepaths = []
    for r,d,f in os.walk('C:\\Users\\Vivek Narayan\\Desktop\\Horizon\\www\\media\\datasets'):
        [image_filepaths.append(str(os.path.join(r,file))) for file in fnmatch.filter(f,'*.nii.gz')]
    
    for img in image_filepaths:
      new_loc = img.replace('.nii.gz','.nrrd')
      sk = sitk.ReadImage(img)
      imgwriter = sitk.ImageFileWriter()
      imgwriter.SetFileName(new_loc)
      imgwriter.SetUseCompression(True)
      imgwriter.Execute(sk)
      os.remove(img)
      
if __name__=="__main__":               
    main()