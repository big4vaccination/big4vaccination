from django.shortcuts import render
from django.views.generic import ListView
from .models import Post
from django.http import HttpResponse
import sqlite3
from sqlite3 import Error
import os
import json
# import pandas as pd 
# import dash 
# import dash_table

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

def create_connection(db):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
 
    return conn

def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM VaccineInfoSet")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
    return rows

def create_connection(db):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
 
    return conn

def advanced_searched(request):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    country_name = request.POST.get('country',False)
    australia_data = "SELECT schedule, vaccine_code, vaccine_desc from VaccineInfoSet where country_name = 'Australia'"
    excute_sentence = "SELECT country_name, schedule, vaccine_code, vaccine_desc from VaccineInfoSet where country_name = '" + str(country_name) + "'"

    country1 = cur.execute(australia_data)
    rows1 = country1.fetchall()
    slice_1 = int(len(rows1) / 2)
    data1 = rows1[:slice_1]

    country2 = cur.execute(excute_sentence)
    rows2 = country2.fetchall()
    slice_2 = int(len(rows2) / 2)
    data2 = rows2[:slice_2]

    push_data = [{}]
    if country_name:
        for i in range(len(data1)):
            push_data[i]["Country Name"] = country_name
            push_data[i]["Vaccine Code"] = data1[i][1]
            push_data[i]["AU Schedule"] = data1[i][0]
            push_data[i][(str(country_name) + " Schedule")] = ""
            push_data[i]["Description"] = data1[i][2]
            push_data.append({})
            for j in range(len(data2)):
                if data1[i][1] == data2[j][2]:
                    push_data[i][(str(country_name) + " Schedule")] = data2[j][1]

    return render(request,'advanced_search.html',{'data':json.dumps(list(push_data))})  # using json.dumps to push the data, using render to pass the content to htmlfile

def Australia_vaccine(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    australia_data = "SELECT country_name, vaccine_code, schedule, vaccine_desc from VaccineInfoSet where country_name = 'Australia'"
    country1 = cur.execute(australia_data)
    rows = country1.fetchall()
    slice_ = int(len(rows) / 2)
    data1 = rows[:slice_]

    push_data = [{}]
    if data1:
        for i in range(len(data1)):
            push_data[i]["Country Name"] = data1[i][0]
            push_data[i]["Vaccine Code"] = data1[i][1]
            push_data[i]["AU Schedule"] = data1[i][2]
            push_data[i]["Description"] = data1[i][3]
            push_data.append({})

    return render(request,'quick_search.html',{'data':json.dumps(list(push_data))})



    # cur = create_connection()
    # cur = request.cursor()
    # cur.execute("SELECT * FROM VaccineInfoSet")
 
    # rows = cur.fetchall()
    # row = cur.fetchone()
    # return HttpResponse(str(row))
    # for row in rows:
    #     print(row)

#     row = cursor.fetchone()

### this is the test code for db
# from django.http import HttpResponse
# import pyodbc
# server = 'big4vaccine.database.windows.net'
# database = 'big4Vaccination'
# username = 'keepdreamlive'
# password = 'woai1ban.'
# driver= '{ODBC Driver 17 for SQL Server}'
# cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()


# def index(request):
#     cursor.execute('SELECT * FROM VaccineInfoSet')
#     row = cursor.fetchone()
#     return HttpResponse(str(row))