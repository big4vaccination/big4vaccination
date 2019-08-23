from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vaccine_Compare

# show the data
admin.site.register(Vaccine_Compare)