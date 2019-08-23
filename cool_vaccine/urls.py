from django.urls import path

from . import views

app_name ='cool_vaccine'

urlpatterns =[
    path('',views.index,name='index'),
    path('', views.child_vaccine_schedule,name='child_vaccine_schedule'),
]