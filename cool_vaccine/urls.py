from django.urls import path

from cool_vaccine import views

urlpatterns =[
    path('',views.index,name='index'),
]