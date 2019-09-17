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
    template_name = 'about_us.html'


class faq(ListView):
    model = Post
    template_name = 'faq.html'


class language(ListView):
    model = Post
    template_name = 'language.html'


def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, '404.html', data)


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
    country_name = request.POST.get('country', False)

    # age = request.POST.get('age', False)
    # australia_data = "SELECT schedule, vaccine_code, vaccine_desc, comments from Vaccine_Info where country_name = 'Australia' and tag = '" + str(age) +"'"
    # australia_data = "SELECT schedule, vaccine_name,Diseases,vaccine_desc, comments, Rating from all_schedule_30 where country_name = 'Australia' order by Rating"
    # excute_sentence = "SELECT country_name, schedule, vaccine_code, comments from Vaccine_Info where country_name = '" + str(country_name) + "'"

    ## Here is for adding the SQLite Query
    excute_sentence = "SELECT * from all_schedule_vs_aus_schedule where country_name = '" + str(country_name) + "'"
    excute_sentence_disease = "SELECT * from diseases_who where Country = '" + str(
        country_name) + "' order by Percentageofreportedcases DESC"

    ## Here is for generating data content
    country_disease = cur.execute(excute_sentence_disease)
    data_disease = country_disease.fetchall()
    compared_data = cur.execute(excute_sentence).fetchall()

    ## Variable -- push_data is for generating second table.
    ##          -- vaccine_desc is not using now
    ##          -- push_disease is for generating first table.
    push_data = [{}]
    # vaccine_desc = [{}]
    push_disease = [{}]

    ## Checking the country name
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

    ## Generating push content for first table and second table
    if country_name:
        ## Generating push content for first table.
        for i in range(len(data_disease)):
            push_disease[i]["Disease name "] = data_disease[i][1]
            if data_disease[i][2] is None:
                push_disease[i]["Number of reported cases in " + str(country_name) + ""] = 0
            else:
                push_disease[i]["Number of reported cases in " + str(country_name) + ""] = data_disease[i][2]
            # push_disease[i]["Average immunisation coverage"]= data_disease[i][3]
            push_disease[i]["Percentage of reported cases in " + str(country_name) + ""] = data_disease[i][4]
            # push_disease[i]["Average immunisation coverage in AU"]= data_disease[i][3]
            if data_disease[i][5] is None:
                push_disease[i]["Number of reported cases in Australia"] = 0
            else:
                push_disease[i]["Number of reported cases in Australia"] = data_disease[i][5]
            push_disease[i]["Percentage of reported cases in Australia"] = data_disease[i][7]

            push_disease.append({})

        ## Generating push content for second table.
        for i in range(len(compared_data)):
            push_data[i]["Vaccine Name"] = compared_data[i][0]
            # if compared_data[i][1] is None:
            #     push_data[i]["Diseases"] = '-'
            # else:
            #     push_data[i]["Diseases"] = compared_data[i][1]

            if compared_data[i][4] and compared_data[i][4] == compared_data[i][19]:
                push_data[i]["Birth"] = "√"
            elif compared_data[i][4] != compared_data[i][19]:
                push_data[i]["Birth"] = "×"
            else:
                push_data[i]["Birth"] = "-"

            if compared_data[i][5] and compared_data[i][5] == compared_data[i][20]:
                push_data[i]["2 mths"] = "√"
            elif compared_data[i][5] != compared_data[i][20]:
                push_data[i]["2 mths"] = "×"
            else:
                push_data[i]["2 mths"] = "-"

            if compared_data[i][6] and compared_data[i][6] == compared_data[i][21]:
                push_data[i]["4 mths"] = "√"
            elif compared_data[i][6] != compared_data[i][21]:
                push_data[i]["4 mths"] = "×"
            else:
                push_data[i]["4 mths"] = "-"

            if compared_data[i][7] and compared_data[i][7] == compared_data[i][22]:
                push_data[i]["6 mths"] = "√"
            elif compared_data[i][7] != compared_data[i][22]:
                push_data[i]["6 mths"] = "×"
            else:
                push_data[i]["6 mths"] = "-"

            if compared_data[i][8] and compared_data[i][8] == compared_data[i][23]:
                push_data[i]["12 mths"] = "√"
            elif compared_data[i][8] != compared_data[i][23]:
                push_data[i]["12 mths"] = "×"
            else:
                push_data[i]["12 mths"] = "-"

            if compared_data[i][9] and compared_data[i][9] == compared_data[i][24]:
                push_data[i]["18 mths"] = "√"
            elif compared_data[i][9] != compared_data[i][24]:
                push_data[i]["18 mths"] = "×"
            else:
                push_data[i]["18 mths"] = "-"

            if compared_data[i][10] and compared_data[i][10] == compared_data[i][25]:
                push_data[i]["2-4 yrs"] = "√"
            elif compared_data[i][10] != compared_data[i][25]:
                push_data[i]["2-4 yrs"] = "×"
            else:
                push_data[i]["2-4 yrs"] = "-"

            if compared_data[i][11] and compared_data[i][11] == compared_data[i][26]:
                push_data[i][">4 yrs"] = "√"
            elif compared_data[i][11] != compared_data[i][26]:
                push_data[i][">4 yrs"] = "×"
            else:
                push_data[i][">4 yrs"] = "-"

            if compared_data[i][12] and compared_data[i][12] == compared_data[i][27]:
                push_data[i]["12-18 yrs"] = "√"
            elif compared_data[i][12] != compared_data[i][27]:
                push_data[i]["12-18 yrs"] = "×"
            else:
                push_data[i]["12-18 yrs"] = "-"

            if compared_data[i][13] and compared_data[i][13] == compared_data[i][28]:
                push_data[i][">18 yrs"] = "√"
            elif compared_data[i][13] != compared_data[i][28]:
                push_data[i][">18 yrs"] = "×"
            else:
                push_data[i][">18 yrs"] = "-"

            if compared_data[i][14] and compared_data[i][14] == compared_data[i][29]:
                push_data[i][">24 yrs"] = "√"
            elif compared_data[i][14] != compared_data[i][29]:
                push_data[i][">24 yrs"] = "×"
            else:
                push_data[i][">24 yrs"] = "-"

            if compared_data[i][15] and compared_data[i][15] == compared_data[i][30]:
                push_data[i][" pg_w"] = "√"
            elif compared_data[i][15] != compared_data[i][30]:
                push_data[i]["pg_w"] = "×"
            else:
                push_data[i]["pg_w"] = "-"

            if compared_data[i][16] and compared_data[i][16] == compared_data[i][31]:
                push_data[i][">=60 yrs"] = "√"
            elif compared_data[i][16] != compared_data[i][31]:
                push_data[i][">=60 yrs"] = "×"
            else:
                push_data[i][">=60 yrs"] = "-"

            push_data.append({})

    ## Generating Return value for frontend
    if country_name == "False" or push_data == [{}] or push_disease == [{}]:
        push_data = [{"Tips": "Select a country, then submit to see the results."}]
        return render(request, 'compare_schedule.html',
                      {'data': json.dumps(list(push_data)), 'country_name': country_name,
                       'disease': json.dumps(list(push_disease)), })
    if country_name and push_data == [{}] or push_disease == [{}]:
        push_data[{"Result": "Sorry, there is no such recording :("}]
        return render(request, 'compare_schedule.html',
                      {'data': json.dumps(list(push_data)), 'country_name': country_name,
                       'disease': json.dumps(list(push_disease)), })
    if country_name and push_data and push_disease:
        return render(request, 'compare_schedule.html',
                      {'data': json.dumps(list(push_data)), 'country_name': country_name,
                       'disease': json.dumps(list(push_disease)), })


def Australia_vaccine(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    # australia_data = "SELECT country_name, vaccine_code, schedule, vaccine_desc from Vaccine_Info where country_name = 'Australia'"
    australia_data = "select * from aus_schedule"
    # australia_data = "SELECT country_name, schedule, vaccine_desc from VaccineInfoSet where country_name = 'Australia'"
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
    # print(data1)
    if data1:
        for i in range(len(data1)):
            push_data[i]["Vaccine name"] = data1[i][0]
            # push_data[i]["Vaccine code"] = data1[i][1]
            # print(type(data1[i][2]))
            if data1[i][2] is None:
                push_data[i]["Diseases"] = "-"
            else:
                push_data[i]["Diseases"] = data1[i][2]
            # push_data[i]["Australian Schedule"] = data1[i][3]
            if data1[i][5] is None:
                push_data[i]["Birth"] = "-"
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                push_data[i]["Birth"] = "✔"
                # push_data[i]["Birth"]=data1[i][5]

            if data1[i][6] is None:
                push_data[i]["2 mths"] = "-"
            else:
                push_data[i]["2 mths"] = "✔"
                # push_data[i]["2 mths"] = data1[i][6]
            if data1[i][7] is None:
                push_data[i]["4 mths"] = "-"
            else:
                push_data[i]["4 mths"] = "✔"
                # push_data[i]["4 mths"] = data1[i][7]
            if data1[i][8] is None:
                push_data[i]["6 mths"] = "-"
            else:
                push_data[i]["6 mths"] = "✔"
                # push_data[i]["6 mths"] = data1[i][8]
=======
                push_data[i]["Birth"]=data1[i][5]
=======
                push_data[i]["Birth"]= "✔"
                #push_data[i]["Birth"]=data1[i][5]
                

>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            if data1[i][6] is None:
                push_data[i]["2 mths"] = "-"
            else:
                push_data[i]["2 mths"] ="✔"
                #push_data[i]["2 mths"] = data1[i][6]
            if data1[i][7] is None:
                push_data[i]["4 mths"] = "-"
            else:
                push_data[i]["4 mths"] ="✔"
                #push_data[i]["4 mths"] = data1[i][7]
            if data1[i][8] is None:
                push_data[i]["6 mths"] = "-"
            else:
<<<<<<< HEAD
                push_data[i]["6 mths"] = data1[i][8]
>>>>>>> parent of 221388b... Children schedule
=======
                push_data[i]["6 mths"] = "✔"
                #push_data[i]["6 mths"] = data1[i][8]
>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            if data1[i][9] is None:
                push_data[i]["12 mths"] = "-"
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                push_data[i]["12 mths"] = "✔"
                # push_data[i]["12 mths"] = data1[i][9]
=======
                push_data[i]["12 mths"] = data1[i][9]
>>>>>>> parent of 221388b... Children schedule
=======
                push_data[i]["12 mths"] ="✔"
                #push_data[i]["12 mths"] = data1[i][9]
>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            if data1[i][10] is None:
                push_data[i]["18 mths"] = "-"
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                push_data[i]["18 mths"] = "✔"
                # push_data[i]["18 mths"] = data1[i][10]
=======
                push_data[i]["18 mths"] = data1[i][10]
>>>>>>> parent of 221388b... Children schedule
=======
                push_data[i]["18 mths"] ="✔"
                #push_data[i]["18 mths"] = data1[i][10]
>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            if data1[i][11] is None:
                push_data[i]["2-4 yrs"] = "-"
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                push_data[i]["2-4 yrs"] = "✔"
                # push_data[i]["2-4 yrs"] = data1[i][11]
=======
                push_data[i]["2-4 yrs"] = data1[i][11]
>>>>>>> parent of 221388b... Children schedule
=======
                push_data[i]["2-4 yrs"]="✔"
                #push_data[i]["2-4 yrs"] = data1[i][11]
>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            if data1[i][12] is None:
                push_data[i][">4 yrs"] = "-"
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                push_data[i][">4 yrs"] = "✔"
                # push_data[i][">4 yrs"] = data1[i][12]
=======
                push_data[i][">4 yrs"] = data1[i][12]
>>>>>>> parent of 221388b... Children schedule
=======
                push_data[i][">4 yrs"] ="✔"
                #push_data[i][">4 yrs"] = data1[i][12]
>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            if data1[i][13] is None:
                push_data[i]["12-18 yrs"] = "-"
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                push_data[i]["12-18 yrs"] = "✔"
                # push_data[i]["12-18 yrs"] = data1[i][13]
=======
                push_data[i]["12-18 yrs"] = data1[i][13]
>>>>>>> parent of 221388b... Children schedule
=======
                push_data[i]["12-18 yrs"] ="✔"
                #push_data[i]["12-18 yrs"] = data1[i][13]
>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            # if data1[i][14] is None:
            #     push_data[i][">18 yrs"]="-"
            # else:
            #     push_data[i][">18 yrs"]=data1[i][14] 
            # if data1[i][15] in None:
            #     push_data[i][">24 yrs"]="-"
            # else:
            #     push_data[i][">24 yrs"]=data1[i][15]
            if data1[i][16] is None:
                push_data[i]["pg_w"] = "-"
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                push_data[i]["pg_w"] = "✔"
                # push_data[i]["pg_w"]=data1[i][16]
=======
                push_data[i]["pg_w"]=data1[i][16]
>>>>>>> parent of 221388b... Children schedule
=======
                push_data[i]["pg_w"]="✔"
                #push_data[i]["pg_w"]=data1[i][16]
>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            if data1[i][17] is None:
                push_data[i][">=60 yrs"] = "-"
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                push_data[i][">=60 yrs"] = "✔"
                # push_data[i][">=60 yrs"]=data1[i][17]

            # push_data[i]["Description"] = data1[i][3]
=======
                 push_data[i][">=60 yrs"]=data1[i][17]
=======
                 push_data[i][">=60 yrs"]="✔"
                 #push_data[i][">=60 yrs"]=data1[i][17]
>>>>>>> 94024388d0add77290afc348d8a911f7030598ad
            
            #push_data[i]["Description"] = data1[i][3]
>>>>>>> parent of 221388b... Children schedule
            push_data.append({})
    # print(push_data)
    # push_data.sort()
    return render(request, 'au_schedule.html', {'data': json.dumps(list(push_data))})


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

    return render(request, 'special_GP.html', {'data': json.dumps(list(push_data)), 'language': language})

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
