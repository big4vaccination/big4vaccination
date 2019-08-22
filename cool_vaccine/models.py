from django.db import models
# import vaccine model
from django.contrib.auth.models import User
# using timezone to manage with time
from django.utils import timezone

# Create your models here.
class vaccine_compare(models.Model):
    # vaccine_name
    vaccine_name = models.CharField(max_length=100)
    # the time of taking vaccination
    vaccine_time = models.IntegerField(50)
    # short_name of vaccine
    short_name_vaccine = models.CharField(max_length = 20)
    # description
    description = models.TextField(max_length=200)
    # country
    country = models.CharField(max_length = 100)
    # is a child
    is_child = models.BooleanField(default=False)

# Create GP entity
class GP(models.Model):
    # address
    address = models.TextField(max_length=200)
    # phone_number
    phone_number = models.IntegerField(20)
