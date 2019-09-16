from django.shortcuts import render, render_to_response
from django.views.generic import ListView
from django.template import RequestContext
from .models import Post
from django.http import HttpResponse
import sqlite3
from sqlite3 import Error
import os
import json
from django.http import Http404

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

def handler404(request):
    response = render_to_response('404.html', {}, context_instance =RequestContext(request) )
    response.status_code = 404
    return response

def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'404.html', data)

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

def disease_on_comparison(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    country_name = request.POST.get('country', False)
    excute_sentence_disease = "SELECT * from disease_proliferation where home_country = '" + str(country_name) + "'"
    country_disease = cur.execute(excute_sentence_disease)
    data_disease = country_disease.fetchall()
    push_data = [{}]
    if country_name == "United Kingdom of Great Britain and Northern Ireland (the)":
        country_name = "England"

    elif country_name == "Philippines (the)":
        country_name = "Philippines"

    elif country_name == "Venezuela (Bolivarian Republic of)":
        country_name = "Venezuela"

    elif country_name == "Iran (Islamic Republic of)":
        country_name = "Iran"

    else:
        country_name = country_name
    if country_name:
        for i in range(len(data_disease)):
            push_data[i]["Disease"] = data_disease[i][4]
            push_data.append({})
    return render(request,'compare_schedule.html',{'data':json.dumps(list(push_data)),'country_name':country_name}) 


def advanced_searched(request):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    country_name = request.POST.get('country', False)
    
    #age = request.POST.get('age', False)
    #australia_data = "SELECT schedule, vaccine_code, vaccine_desc, comments from Vaccine_Info where country_name = 'Australia' and tag = '" + str(age) +"'"
    australia_data = "SELECT schedule, vaccine_code, vaccine_desc, comments from Vaccine_Info where country_name = 'Australia'"
    #excute_sentence = "SELECT country_name, schedule, vaccine_code, comments from Vaccine_Info where country_name = '" + str(country_name) + "'"
    excute_sentence = "SELECT country_name, schedule, vaccine_code, comments from Vaccine_Info where country_name = '" + str(country_name) + "'"
    excute_sentence_disease = "SELECT * from disease_proliferation where home_country = '" + str(country_name) + "'"
    
    country_disease = cur.execute(excute_sentence_disease)
    data_disease = country_disease.fetchall()
    
    country1 = cur.execute(australia_data)
    data1 = country1.fetchall()

    country2 = cur.execute(excute_sentence)
    data2 = country2.fetchall()
    push_data = [{}]
    vaccine_desc = [{}]
    push_disease = [{}]

    if country_name == "United Kingdom of Great Britain and Northern Ireland (the)":
        country_name = "England"

    elif country_name == "Philippines (the)":
        country_name = "Philippines"

    elif country_name == "Venezuela (Bolivarian Republic of)":
        country_name = "Venezuela"

    elif country_name == "Iran (Islamic Republic of)":
        country_name = "Iran"

    else:
        country_name = country_name

    if country_name:
        for i in range(len(data_disease)):
            push_disease[i]["Disease"]= data_disease[i][4]
            push_disease[i]["Average annual cases"]= data_disease[i][5]
            #push_disease[i]["Average immunisation coverage"]= data_disease[i][3]
            push_disease[i]["Average annual cases in AU"]= data_disease[i][7]
            #push_disease[i]["Average immunisation coverage in AU"]= data_disease[i][3]

            push_disease.append({})
        for i in range(len(data1)):
            #push_data[i]["Country Name"] = country_name
            push_data[i]["Vaccine Name"] = data1[i][1]
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
            push_data[i]["AU Schedule"] = data1[i][0]
    print(push_disease)
    #if country_name == "False" or age == "False" or push_data == [{}]:
    if country_name == "False" or push_data == [{}] or push_disease==[{}]:
        push_data = [{"Tips":"Select a country, then submit to see the results."}]

    return render(request,'compare_schedule.html',{'data':json.dumps(list(push_data)),'country_name':country_name,'disease':json.dumps(list(push_disease)),'vaccine_desc':json.dumps(list(vaccine_desc))})  # using json.dumps to push the data, using render to pass the content to htmlfile

def Australia_vaccine(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    #australia_data = "SELECT country_name, vaccine_code, schedule, vaccine_desc from Vaccine_Info where country_name = 'Australia'"
    australia_data="select * from aus_schedule"
    #australia_data = "SELECT country_name, schedule, vaccine_desc from VaccineInfoSet where country_name = 'Australia'"
    country1 = cur.execute(australia_data)
    data1 = country1.fetchall()

    push_data = [{}]
    # if data1:
    #     for i in range(len(data1)):
    #         push_data[i]["Country Name"] = data1[i][0]
    #         push_data[i]["Vaccine Name"] = data1[i][1]
    #         push_data[i]["Australian Schedule"] = data1[i][2]
    #         push_data[i]["Description"] = data1[i][3]
    #         push_data.append({})
    #print(data1)
    if data1:
        for i in range(len(data1)):
            push_data[i]["Vaccine name"] = data1[i][0]
            #push_data[i]["Vaccine code"] = data1[i][1]
            #print(type(data1[i][2]))
            if data1[i][2] is None:
                push_data[i]["Diseases"] = "-"
            else:
                push_data[i]["Diseases"] = data1[i][2]
            #push_data[i]["Australian Schedule"] = data1[i][3]
            if data1[i][5] is None:
                push_data[i]["Birth"] = "-"
            else:
                push_data[i]["Birth"]=data1[i][5]
            if data1[i][6] is None:
                push_data[i]["2 mths"] = "-"
            else:
                push_data[i]["2 mths"] = data1[i][6]
            if data1[i][7] is None:
                push_data[i]["4 mths"] = "-"
            else:
                push_data[i]["4 mths"] = data1[i][7]
            if data1[i][8] is None:
                push_data[i]["6 mths"] = "-"
            else:
                push_data[i]["6 mths"] = data1[i][8]
            if data1[i][9] is None:
                push_data[i]["12 mths"]="-"
            else:
                push_data[i]["12 mths"] = data1[i][9]
            if data1[i][10] is None:
                push_data[i]["18 mths"]="-"
            else:
                push_data[i]["18 mths"] = data1[i][10]
            if data1[i][11] is None:
                push_data[i]["2-4 yrs"]="-"
            else:
                push_data[i]["2-4 yrs"] = data1[i][11]
            if data1[i][12] is None:
                push_data[i][">4 yrs"]= "-"
            else:
                push_data[i][">4 yrs"] = data1[i][12]
            if data1[i][13] is None:
                push_data[i]["12-18 yrs"]="-"
            else:
                push_data[i]["12-18 yrs"] = data1[i][13]
            # if data1[i][14] is None:
            #     push_data[i][">18 yrs"]="-"
            # else:
            #     push_data[i][">18 yrs"]=data1[i][14] 
            # if data1[i][15] in None:
            #     push_data[i][">24 yrs"]="-"
            # else:
            #     push_data[i][">24 yrs"]=data1[i][15]
            if data1[i][16] is None:
                push_data[i]["pg_w"]="-"
            else:
                push_data[i]["pg_w"]=data1[i][16]
            if data1[i][17] is None:
                push_data[i][">=60 yrs"]="-"
            else:
                 push_data[i][">=60 yrs"]=data1[i][17]
            
            #push_data[i]["Description"] = data1[i][3]
            push_data.append({})
    #print(push_data)
    # push_data.sort()
    return render(request,'au_schedule.html',{'data':json.dumps(list(push_data))})

def find_GP(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    language = request.POST.get('language', False)
    sentence = "SELECT lat,lng from gp_data where language = '" + str(language) + "'"
    gp_data = cur.execute(sentence).fetchall()

    push_data = [{}]
    if gp_data:
        for i in range(len(gp_data)):
            push_data[i]["lat"] = gp_data[i][0]
            push_data[i]["lng"] = gp_data[i][1]
            push_data.append({})

    return render(request,'special_GP.html',{'data':json.dumps(list(push_data)),'language':language})

# def takeSecond(elem):
#     return elem[2]

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