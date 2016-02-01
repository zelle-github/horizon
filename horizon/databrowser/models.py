from __future__ import unicode_literals

from django.db import models

import datetime
from django.utils import timezone
from dicom import datadict

# Create your models here.
class Dataset(models.Model):
    datasetid = models.AutoField(primary_key=True)
    dataset_name = models.CharField(max_length=200)
    
    dataset_rootpath = models.FilePathField(max_length=500,blank=True)
    
    dataset_startdate = models.DateTimeField("date initialized", default=timezone.now, blank=True)
    dataset_description = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return unicode(self.dataset_name)
    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Dataset._meta.fields]

class Patient(models.Model):
    patientid = models.AutoField(primary_key=True)
    fk_patient_dataset = models.ForeignKey(Dataset)
    
    patient_rootpath = models.FilePathField(max_length=500,blank=True)
    patient_dicomid = models.CharField(max_length=200, default="Anonymized")

    def __unicode__(self):
        return unicode(self.pk)
        
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Patient._meta.fields]
        
class Study(models.Model):
    studyid = models.AutoField(primary_key=True)
    fk_study_patient = models.ForeignKey(Patient)
    
    study_rootpath = models.FilePathField(max_length=500,blank=True)
    study_name = models.CharField(max_length=200, default="Unknown Study")
    #study_description = models.CharField(max_length=200, default="Unknown Study")
    
    def __unicode__(self):
        return unicode(self.pk)
        
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Study._meta.fields]          
        
class Image(models.Model):      
    imageid = models.AutoField(primary_key=True)
    fk_image_study = models.ForeignKey(Study)
    
    image_filepath = models.FilePathField(max_length=500)
    image_name = models.CharField(max_length=200, default="Unknown")

    image_spaceorigin = models.CharField(max_length=200, default="Unknown")
    image_endian = models.CharField(max_length=200, default="Unknown")
    image_spacedirections = models.CharField(max_length=200, default="Unknown")
    image_space = models.CharField(max_length=200, default="Unknown")
    image_sizes = models.CharField(max_length=200, default="Unknown")
    image_encoding = models.CharField(max_length=200, default="Unknown")
    image_nrrdname = models.CharField(max_length=200, default="Unknown")
    image_kinds = models.CharField(max_length=200, default="Unknown")
    image_type = models.CharField(max_length=200, default="Unknown")
    image_dimension = models.CharField(max_length=200, default="Unknown")

    def __unicode__(self):
        return unicode(self.pk)
    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Image._meta.fields]
        
class Segmentation(models.Model):
    VALIDATION = (
          ("1", "Missing"),
          ("2", "Invalidated"),
          ("3", "Validated"),
    )

    segmentationid = models.AutoField(primary_key=True)
    fk_segmentation_image = models.ForeignKey(Image)
    
    segmentation_filepath = models.FilePathField(max_length=500)
    segmentation_name = models.CharField(max_length=200, default="Unknown")
    
    segmentation_spaceorigin = models.CharField(max_length=200, default="Unknown")
    segmentation_endian = models.CharField(max_length=200, default="Unknown")
    segmentation_spacedirections = models.CharField(max_length=200, default="Unknown")
    segmentation_space = models.CharField(max_length=200, default="Unknown")
    segmentation_sizes = models.CharField(max_length=200, default="Unknown")
    segmentation_encoding = models.CharField(max_length=200, default="Unknown")
    segmentation_nrrdname = models.CharField(max_length=200, default="Unknown")
    segmentation_kinds = models.CharField(max_length=200, default="Unknown")
    segmentation_type = models.CharField(max_length=200, default="Unknown")
    segmentation_dimension = models.CharField(max_length=200, default="Unknown")
    
    ##segmentation_segmentationobjectname = models.CharField(max_length=200, default="Tumor")
    ##fk_segmentation_segmentationradiologist = models.ForeignKey(Radiologist, default="Unknown", related_name="contributor")
    ##segmentation_segmentationdate = models.DateTimeField("date segmentated", default=timezone.now, blank=True)
    
    segmentation_validationstatus = models.CharField(max_length=1, choices=VALIDATION, default="2")
    ##fk_segmentation_validationradiologist = models.ForeignKey(Radiologist, default="Unknown", related_name="validator")
    ##segmentation_validationdate = models.DateTimeField("date validated", blank=True)
    
    #fk_segmentation_dicommetadata = models.ForeignKey(DICOMMetadata, null=True)
    
    def __unicode__(self):
        return unicode(self.pk)
        
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Segmentation._meta.fields]

"""        
class NRRDImageContourSnapshot(models.Model):
    nrrdimagecontoursnapshotid = models.AutoField(primary_key=True)
    fk_nrrdimagecontoursnapshot_nrrdimage = models.ForeignKey(NRRDImage)
    fk_nrrdimagecontoursnapshot_contour = models.ForeignKey(Contour)
    
    nrrdimagecontoursnapshot_imagefile = models.ImageField(max_length=500)
    
    def __unicode__(self):
        return unicode(self.fk_nrrdimagecontoursnapshot_contour)
        
    class Meta:
        index_together = ("fk_nrrdimagecontoursnapshot_nrrdimage", "fk_nrrdimagecontoursnapshot_contour")
    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in NRRDImageContourSnapshot._meta.fields]
        
class DICOMMetadata(models.Model):
    dicommetadataid = models.AutoField(primary_key=True)    
    
    #use dicomheaderparser to create tables and load data for each dicomseries id)
    headerTagDict = datadict.keyword_dict
    specialHeaderFields = ["FileCount","PatientName","PatientID","StudyID","StudyDate","StudyDescription","SeriesInstanceUID","SeriesDate","SeriesDescription","Modality","SliceThickness","PixelSpacing"]
    specialHeaderFields = [header.lower() for header in specialHeaderFields]
    for headerField in headerTagDict.keys():
        headerfieldlower = str(headerField).lower()
        if len(headerfieldlower) > 55: 
            headerfieldlower = headerfieldlower[:55]
            
        if headerfieldlower in specialHeaderFields:
            locals()[("dicom_%s") %(headerfieldlower)] = models.CharField(max_length=100, default="None") 
    
    for headerField in headerTagDict.keys()[:100]:
        headerfieldlower = str(headerField).lower()
        if len(headerfieldlower) > 55: 
            headerfieldlower = headerfieldlower[:55]
        elif headerfieldlower != '' and headerfieldlower is not None:
            locals()[("dicom_%s") %(headerfieldlower)] = models.CharField(max_length=100, default="None") 

    def __unicode__(self):
        return unicode(self.pk)
        
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in DICOMMetadata._meta.fields]
        
class DICOMSeriesFile(models.Model):
    dicomseriesfileid = models.AutoField(primary_key=True)
    fk_dicomseriesfile_dicommetadata = models.ForeignKey(DICOMMetadata)
    
    fk_dicomseriesfile_patient = models.ForeignKey(Patient)
    fk_dicomseriesfile_dataset = models.ForeignKey(Dataset)
    
    dicomseriesfile_filepath = models.FilePathField(max_length=500)
    
    def __unicode__(self):
        return unicode(self.pk)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in DICOMSeriesFile._meta.fields]
""" 
       
"""
class AuthUsers(models.Model):
    USERTYPE = (
          ('1', 'Guest'),
          ('2', 'Researcher'),
          ('3', 'Clinical Investigator'),
          ('4', 'Clinician'),
          ('5', 'Radiologist'),
          ('6', 'Radiation Oncologist'),
          ('7', 'Principle Investigator'),
          ('8', 'Administrator'),  
    )
    authuserid = models.AutoField(primary_key=True)
    authuser_username = models.CharField(max_length=200, unique=True)
    authuser_password = models.CharField(max_length=200) #use md5 encryption on insert
    authuser_usertype = models.CharField(max_length=2, choices=USERTYPE, default='1')
    authuser_fname = models.CharField(max_length=200)
    authuser_lname = models.CharField(max_length=200)
    authuser_email = models.CharField(max_length=200)
    authuser_phone = models.CharField(max_length=200, blank=True)
    authuser_institution = models.CharField(max_length=200, blank=True)
    # permitteddatasets (set of dataset ids)
    
    def __unicode__(self):
        return self.username

class Radiologist(models.Model):
    radiologistid = models.AutoField(primary_key=True)
    fk_radiologist_authusername = models.ForeignKey(AuthUsers, to_field='authuser_username', )
    radiologist_specialty = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return fk_radiologist_authusername
"""
        
"""
class RadiomicsFeatureVectorParameters(models.Model):
    INTERPOLATIONS = (
          ('1', 'raw')
          ('2', '1x1x1')
          ('3', '2x2x2')
          ('4', '3x3x3')
    )
    featurevectorid (fk not null)
    filepath
    nrrdseriesid (fk not null)
    contourseriesid (fk not null)
    dicomseriesid
    datasetid (set)
    matlaborpython
    toolboxversion
    intensitynormalization (default to 0)
    sliceinterpolation (default to '4')
    binwdith (default to 25)
    glcm_neighborhood_radius (default to 1)
    ...other parameter fields

class RadiomicsFeatureVector(models.Model):
    featurevectorid  = models.AutoField(primary_key=True)
    #use python to set all feature vector fields
"""