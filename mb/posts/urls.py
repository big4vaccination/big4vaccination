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
from .views import HomePageView, About_us, faq
from .views import advanced_searched, Australia_vaccine

urlpatterns = [
    path('faq', faq.as_view(), name = 'faq'),
    path('about_us', About_us.as_view(), name = 'about_us'),
    path('', HomePageView.as_view(), name = 'home'),
<<<<<<< HEAD
    path('advanced_search', advanced_searched,name= 'advanced_search'),
=======
    path('advanced_search', index, name='advanced_search'),
>>>>>>> d39682d09256a6c62856834eb02a41ec2d1b12da
    path('quick_search', Australia_vaccine, name='quick_search'),
]
