from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from django.template import RequestContext, loader
from django.http import Http404

import json
import collections
import os
import glob
import SimpleITK as sitk

from .models import *

# Create your views here.
#def index(request):
#    return render_to_response('databrowser/index.html')

def index(request):    
    datasets = {}
    
    for dataset in Dataset.objects.all():
        datasets[dataset.pk] = {'dataset': dataset, 'patients': {}}                           
        patients = dataset.patient_set.all()
        for patient in patients:
            datasets[dataset.pk]['patients'] \
                                [patient.pk] = {'patient': patient, 
                                                'studies': {}}                                       
            studies = patient.study_set.all()
            for study in studies:
                datasets[dataset.pk]['patients'] \
                                    [patient.pk]['studies'] \
                                    [study.pk] = {'study': study,
                                                  'images': {}}
                images = study.image_set.all()
                for image in images:
                    segmentations = image.segmentation_set.all()                  
                    datasets[dataset.pk]['patients'] \
                                        [patient.pk]['studies'] \
                                        [study.pk]['images'] \
                                        [image.pk ] = {'image': image,
                                                      'segmentations': segmentations}
                                                      
    context = {'datasets': datasets}
    return render(request, 'databrowser/index.html', context)