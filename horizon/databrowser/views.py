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
import numpy
import SimpleITK as sitk
import base64
import pdb

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

    
def generate_images(request):
    if request.method == 'POST':
        image_pk = str(request.POST.get('image_id'))
        print image_pk
        image = Image.objects.get(pk=image_pk)
        image_path = str(image.image_filepath)
        
        #pdb.set_trace()
        
        image_sitk = sitk.ReadImage(image_path)
        imagearray_sitk = sitk.GetArrayFromImage(image_sitk)
        
        arrays_base64 = collections.OrderedDict()
        for index, slice in enumerate(imagearray_sitk):
          ind = str(index)
          arrays_base64[ind] = {}
          arr = base64.b64encode(slice)
          arrays_base64[ind]['array'] = arr
          arrays_base64[ind]['min'] = numpy.asscalar(imagearray_sitk.min())
          arrays_base64[ind]['max'] = numpy.asscalar(imagearray_sitk.max())
          arrays_base64[ind]['column_spacing'] = image_sitk.GetSpacing()[0]
          arrays_base64[ind]['row_spacing'] = image_sitk.GetSpacing()[1]
          arrays_base64[ind]['width'] = image_sitk.GetSize()[0]
          arrays_base64[ind]['height'] = image_sitk.GetSize()[1]
          
        slices = len(arrays_base64.keys())
        
        return HttpResponse(
          json.dumps({"slices": str(slices-1),
                      "arrays": arrays_base64}),
          content_type="application/json"
      )
    
    else:
      return HttpResponse(
          json.dumps({"FAILED": "this isn't happening"}),
          content_type="application/json"
      )    