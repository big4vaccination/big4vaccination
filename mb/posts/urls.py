"""mb_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import handler404, handler500
from .views import HomePageView, About_us, faq, handler404, error_404_view
from .views import advanced_searched, Australia_vaccine,find_GP, language, first_intepreting,second_intepreting,third_intepreting,check_box, free_au_vaccine



urlpatterns = [
    path('faq', faq.as_view(), name = 'faq'),
    path('language', language.as_view(), name = 'language'),
    path('about_us', About_us.as_view(), name = 'about_us'),
    path('', HomePageView.as_view(), name = 'home'),

    path('compare_schedule', advanced_searched,name= 'compare_schedule'),

    path('au_schedule', Australia_vaccine, name='au_schedule'),
    path('free_au_vaccine',free_au_vaccine,name='free_au_vaccine'),

    path('check',check_box,name='check_box'),

    path('special_GP',find_GP,name='special_GP'),
    path('first_intepreting', first_intepreting.as_view(), name = 'first_intepreting'),
    path('second_intepreting', second_intepreting.as_view(), name = 'second_intepreting'),
    path('third_intepreting', third_intepreting.as_view(), name = 'third_intepreting'),
]

handler404 = error_404_view
handler404 = error_404_view