from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

#Add this code:
from django.template import RequestContext, loader
from django.http import Http404

# Create your views here.
def index(request):
    return render_to_response('home/index.html')