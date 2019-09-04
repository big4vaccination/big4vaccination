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
    age = request.POST.get('age',False)
    australia_data = "SELECT schedule, vaccine_code, vaccine_desc, comments from Vaccine_Info where country_name = 'Australia' and tag = '" + str(age) +"'"
    excute_sentence = "SELECT country_name, schedule, vaccine_code, comments from Vaccine_Info where country_name = '" + str(country_name) + "'"

    country1 = cur.execute(australia_data)
    data1 = country1.fetchall()

    country2 = cur.execute(excute_sentence)
    data2 = country2.fetchall()
    push_data = [{}]
    vaccine_desc = [{}]

    if country_name == "United Kingdom of Great Britain and Northern Ireland (the)":
        country_name = "England"

    elif country_name == "Philippines (the)":
        country_name = "Philippines"

    elif country_name == "United States of America (the)":
        country_name = "United States of Amerca"

    elif country_name == "Iran (Islamic Republic of)":
        country_name = "Iran"

    elif country_name == "False":
        country_name = ""
    else:
        country_name = country_name

    if country_name:
        for i in range(len(data1)):
            push_data[i]["Country Name"] = country_name
            push_data[i]["Vaccine Name"] = data1[i][1]
            push_data[i]["AU Schedule"] = data1[i][0]
            push_data[i][(str(country_name) + " Schedule")] = "-"
            if data1[i][3] == "0":
                vaccine_desc[i]["Description"] = data1[i][2] + "\n\n"
            else:
                vaccine_desc[i]["Description"] = data1[i][2] + ", " + data1[i][3]
            push_data.append({})
            vaccine_desc.append({})
            for j in range(len(data2)):
                if data1[i][1] == data2[j][2]:
                    push_data[i][(str(country_name) + " Schedule")] = data2[j][1]
    if push_data == [{}]:
        push_data = [{"result":"No such record"}]

    return render(request,'compare_schedule.html',{'data':json.dumps(list(push_data)),'country_name':country_name,'age':age,'vaccine_desc':json.dumps(list(vaccine_desc))})  # using json.dumps to push the data, using render to pass the content to htmlfile

def Australia_vaccine(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    australia_data = "SELECT country_name, vaccine_code, schedule, vaccine_desc from Vaccine_Info where country_name = 'Australia'"
    #australia_data = "SELECT country_name, schedule, vaccine_desc from VaccineInfoSet where country_name = 'Australia'"
    country1 = cur.execute(australia_data)
    data1 = country1.fetchall()

    push_data = [{}]
    if data1:
        for i in range(len(data1)):
            push_data[i]["Country Name"] = data1[i][0]
            push_data[i]["Vaccine Name"] = data1[i][1]
            push_data[i]["Australian Schedule"] = data1[i][2]
            push_data[i]["Description"] = data1[i][3]
            push_data.append({})

    return render(request,'au_schedule.html',{'data':json.dumps(list(push_data))})



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