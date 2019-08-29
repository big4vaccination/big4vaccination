from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# Create your views here.
class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'all_posts_list'

class About_us(ListView):
    model = Post
    template_name='about_us.html'

class faq(ListView):
    model = Post
    template_name='faq.html'
    
### this is the test code for db
from django.http import HttpResponse
import pyodbc
server = 'big4vaccine.database.windows.net'
database = 'big4Vaccination'
username = 'keepdreamlive'
password = 'woai1ban.'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


def index(request):
    cursor.execute('SELECT * FROM VaccineInfoSet')
    row = cursor.fetchone()
    return HttpResponse(str(row))