from django.shortcuts import render
from django.template import loader
# Create your views here.
from django.http import HttpResponse
# import vaccine_compare db
from .models import Vaccine_Compare
from django.http import Http404

# Test function can be hidden
def index(request):
    return HttpResponse('Hello big4. this is a test.')

# return the child vaccine schedule
def child_vaccine_schedule(request,flag):
    vaccine_list = Vaccine_Compare.objects.filter(is_child=flag)
    context = {
        'vaccine schedule': vaccine_list
    }
    return render(request, 'cool_vaccine/index.html',context)

