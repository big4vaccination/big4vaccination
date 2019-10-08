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

class first_intepreting(ListView):
    model= Post
    template_name = 'first_intepreting.html'

class second_intepreting(ListView):
    model= Post
    template_name = 'second_intepreting.html'

class third_intepreting(ListView):
    model= Post
    template_name = 'third_intepreting.html'

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
    country_name = request.POST.get('country',"Select")

    # age = request.POST.get('age', False)
    # australia_data = "SELECT schedule, vaccine_code, vaccine_desc, comments from Vaccine_Info where country_name = 'Australia' and tag = '" + str(age) +"'"
    # australia_data = "SELECT schedule, vaccine_name,Diseases,vaccine_desc, comments, Rating from all_schedule_30 where country_name = 'Australia' order by Rating"
    # excute_sentence = "SELECT country_name, schedule, vaccine_code, comments from Vaccine_Info where country_name = '" + str(country_name) + "'"

    ## Here is for adding the SQLite Query
    excute_sentence = "SELECT DISTINCT * from compare_data where country_name = '" + str(country_name) + "' order by vaccine_name ASC"
    vaccine_name = "SELECT DISTINCT vaccine_name from compare_data where country_name = '" + str(country_name) + "' order by vaccine_name ASC"
    australia = "SELECT DISTINCT * from aus_schedule order by vaccine_name ASC"
    compared_data = cur.execute(excute_sentence).fetchall()
    australia_vaccine_list = cur.execute(australia).fetchall()
    other_vaccine_list = cur.execute(vaccine_name).fetchall()
    other = []
    au_vaccine = []

    for i in other_vaccine_list:
        other.append(i[0])

    for i in australia_vaccine_list:
        au_vaccine.append(i[15])
    ## Variable -- push_data is for generating second table.
    ##          -- vaccine_desc is not using now
    ##          -- push_disease is for generating first table.
    ##          -- out_put is for final out_put
    ##          -- out_put2 is for final out_put2
    push_data = [{}]
    # vaccine_desc = [{}]
    push_disease = [{}]
    out_put = []
    out_put2 = []

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

    excute_sentence_disease = "SELECT * from diseases_who where Country = '" + str(
        country_name) + "' order by Percentageofreportedcases DESC"

    ## Here is for generating data content
    country_disease = cur.execute(excute_sentence_disease)
    data_disease = country_disease.fetchall()

    ## Generating push content for first table and second table
    if country_name != "Select":
        ## Generating push content for first table.
        for i in range(len(data_disease)):
            if data_disease[i][2] != "0" and data_disease[i][2] is not None:
                push_disease[i]["Disease Name"] = data_disease[i][1]
                push_disease[i]["% of Reported cases in " + str(country_name) + ""] = data_disease[i][5]
                # push_disease[i]["Average immunisation coverage"]= data_disease[i][3]
                # push_disease[i]["Percentage of reported cases in " + str(country_name) + ""] = data_disease[i][4]
                # push_disease[i]["Average immunisation coverage in AU"]= data_disease[i][3]
                push_disease[i]["% of Reported cases in Australia"] = data_disease[i][8]
            # push_disease[i]["Percentage of reported cases in Australia"] = data_disease[i][7]

            push_disease.append({})

        ## Generating push content for second table.
        for i in range(len(compared_data)):
            if compared_data[i][0] and compared_data[i][0] in au_vaccine:
                push_data[i]["Vaccine Name"] = compared_data[i][0]
                # if compared_data[i][1] is None:
                #     push_data[i]["Diseases"] = '-'
                # else:
                #     push_data[i]["Diseases"] = compared_data[i][1]
                if compared_data[i][4] and compared_data[i][4] == compared_data[i][18]:
                    push_data[i]["Birth"] = "✔"
                elif compared_data[i][4] and compared_data != compared_data[i][18]:
                    push_data[i]["Birth"] = "Χ"
                else:
                    push_data[i]["Birth"] = ""

                if compared_data[i][5] and compared_data[i][5] == compared_data[i][19]:
                    push_data[i]["2 mths"] = "✔"
                elif compared_data[i][5] and compared_data != compared_data[i][19]:
                    push_data[i]["2 mths"] = "Χ"
                else:
                    push_data[i]["2 mths"] = ""

                if compared_data[i][6] and compared_data[i][6] == compared_data[i][20]:
                    push_data[i]["4 mths"] = "✔"
                elif compared_data[i][6] and compared_data != compared_data[i][20]:
                    push_data[i]["4 mths"] = "Χ"
                else:
                    push_data[i]["4 mths"] = ""

                if compared_data[i][7] and compared_data[i][7] == compared_data[i][21]:
                    push_data[i]["6 mths"] = "✔"
                elif compared_data[i][7] and compared_data != compared_data[i][21]:
                    push_data[i]["6 mths"] = "Χ"
                else:
                    push_data[i]["6 mths"] = ""

                if compared_data[i][8] and compared_data[i][8] == compared_data[i][22]:
                    push_data[i]["12 mths"] = "✔"
                elif compared_data[i][8] and compared_data != compared_data[i][22]:
                    push_data[i]["12 mths"] = "Χ"
                else:
                    push_data[i]["12 mths"] = ""

                if compared_data[i][9] and compared_data[i][9] == compared_data[i][23]:
                    push_data[i]["18 mths"] = "✔"
                elif compared_data[i][9] and compared_data != compared_data[i][23]:
                    push_data[i]["18 mths"] = "Χ"
                else:
                    push_data[i]["18 mths"] = ""

                if compared_data[i][10] and compared_data[i][10] == compared_data[i][24]:
                    push_data[i]["2-4 yrs"] = "✔"
                elif compared_data[i][10] and compared_data != compared_data[i][24]:
                    push_data[i]["2-4 yrs"] = "Χ"
                else:
                    push_data[i]["2-4 yrs"] = ""

                if compared_data[i][11] and compared_data[i][11] == compared_data[i][25]:
                    push_data[i][">4 yrs"] = "✔"
                elif compared_data[i][11] and compared_data != compared_data[i][25]:
                    push_data[i][">4 yrs"] = "Χ"
                else:
                    push_data[i][">4 yrs"] = ""

                if compared_data[i][12] and compared_data[i][12] == compared_data[i][26]:
                    push_data[i]["12-18 yrs"] = "✔"
                elif compared_data[i][12] and compared_data != compared_data[i][26]:
                    push_data[i]["12-18 yrs"] = "Χ"
                else:
                    push_data[i]["12-18 yrs"] = ""

                if compared_data[i][13] and compared_data[i][13] == compared_data[i][27]:
                    push_data[i][">18 yrs"] = "✔"
                elif compared_data[i][13] and compared_data != compared_data[i][27]:
                    push_data[i][">18 yrs"] = "Χ"
                else:
                    push_data[i][">18 yrs"] = ""

                if compared_data[i][14] and compared_data[i][14] == compared_data[i][28]:
                    push_data[i][">24 yrs"] = "✔"
                elif compared_data[i][14] and compared_data != compared_data[i][28]:
                    push_data[i][">24 yrs"] = "Χ"
                else:
                    push_data[i][">24 yrs"] = ""

                # if compared_data[i][15] and compared_data[i][15] == compared_data[i][30]:
                #     push_data[i]["pg_w"] = "✔"
                # elif compared_data[i][15] and compared_data != compared_data[i][30]:
                #     push_data[i]["pg_w"] = "Χ"
                # else:
                #     push_data[i]["pg_w"] = ""

                if compared_data[i][16] and compared_data[i][16] == compared_data[i][30]:
                    push_data[i][">=60 yrs"] = "✔"
                elif compared_data[i][16] and compared_data != compared_data[i][30]:
                    push_data[i][">=60 yrs"] = "Χ"
                else:
                    push_data[i][">=60 yrs"] = ""

            push_data.append({})

        # for generating unmatched vaccine
        for i in range(len(australia_vaccine_list)):
            temp = {}
            if australia_vaccine_list[i][15] not in other:
                temp["Vaccine Name"] = australia_vaccine_list[i][15]
                if australia_vaccine_list[i][2]:
                    temp["Birth"] = "Χ"
                else:
                    temp["Birth"] = ""

                if australia_vaccine_list[i][3]:
                    temp["2 mths"] = "Χ"
                else:
                    temp["2 mths"] = ""

                if australia_vaccine_list[i][4]:
                    temp["4 mths"] = "Χ"
                else:
                    temp["4 mths"] = ""

                if australia_vaccine_list[i][5]:
                    temp["6 mths"] = "Χ"
                else:
                    temp["6 mths"] = ""

                if australia_vaccine_list[i][6]:
                    temp["12 mths"] = "Χ"
                else:
                    temp["12 mths"] = ""

                if australia_vaccine_list[i][7]:
                    temp["18 mths"] = "Χ"
                else:
                    temp["18 mths"] = ""

                if australia_vaccine_list[i][8]:
                    temp["2-4 yrs"] = "Χ"
                else:
                    temp["2-4 yrs"] = ""

                if australia_vaccine_list[i][9]:
                    temp[">4 yrs"] = "Χ"
                else:
                    temp[">4 yrs"] = ""

                if australia_vaccine_list[i][10]:
                    temp["12-18 yrs"] = "Χ"
                else:
                    temp["12-18 yrs"] = ""

                if australia_vaccine_list[i][11]:
                    temp[">18 yrs"] = "Χ"
                else:
                    temp[">18 yrs"] = ""

                if australia_vaccine_list[i][12]:
                    temp[">24 yrs"] = "Χ"
                else:
                    temp[">24 yrs"] = ""

                # if australia_vaccine_list[i][16]:
                #     temp["pg_w"] = "Χ"
                # else:
                #     temp["pg_w"] = ""

                if australia_vaccine_list[i][13]:
                    temp[">=60 yrs"] = "Χ"
                else:
                    temp[">=60 yrs"] = ""
            if temp is not None:
                push_data.append(temp)
           # sorted (push_data.keys(vaccine_name))

        # for generating final output by A-Z order
        for i in push_data:
            if i != {}:
                out_put.append(i)
        out_put = sorted(out_put, key=lambda e:e['Vaccine Name'],reverse=False)

        # for generating final output by A-Z order
        for i in push_disease:
            if i != {}:
                out_put2.append(i)
        out_put2 = sorted(out_put2, key=lambda e:e['Disease Name'],reverse=False)

    ## Generating Return value for frontend
    if country_name == "Select" and out_put == [] and out_put2 == []:
        return render(request, 'compare_schedule.html',
                      {'data': json.dumps(list(out_put)), 'country_name': country_name,
                       'disease': json.dumps(list(out_put2)), })
    elif country_name and out_put == [] and out_put2 == []:
        # push_data["Result"] =  "Sorry, there is no such recording :("
        return render(request, 'compare_schedule.html',
                      {'data': json.dumps(list(out_put)), 'country_name': country_name,
                       'disease': json.dumps(list(out_put2)), })
    elif country_name != False and out_put and out_put2:
        return render(request, 'compare_schedule.html',
                      {'data': json.dumps(list(out_put)), 'country_name': country_name,
                       'disease': json.dumps(list(out_put2)), 'explanation': "Percentage of Reported Cases in 2018 year per 100,000",
                       "comparison": "Comparison of Vaccine Schedules","right":" √ Vaccine is recommended in "+ str(country_name) +"",
                       "wrong":"Χ Vaccine is optional in "+ str(country_name) +", but recommended in Australia."})


def Australia_vaccine(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    # australia_data = "SELECT country_name, vaccine_code, schedule, vaccine_desc from Vaccine_Info where country_name = 'Australia'"
    australia_data = "select * from aus_schedule"
    # australia_data = "SELECT country_name, schedule, vaccine_desc from VaccineInfoSet where country_name = 'Australia'"
    country1 = cur.execute(australia_data)
    data1 = country1.fetchall()
    # data2=country1.fetchall()
    push_data = [{}]
    disease_data = [{}]
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
            push_data[i]["Vaccine Name"] = data1[i][15]
            disease_data[i]["Vaccine Name"] = data1[i][15]
            # push_data[i]["Vaccine code"] = data1[i][1]
            # print(type(data1[i][2]))
            if data1[i][16] is None:
                disease_data[i]["Diseases"] = "-"
            else:
                disease_data[i]["Diseases"] = data1[i][16]
            # if data1[i][4] is None:
            #     disease_data[i]["Description"] = "-"
            # else:
            #     disease_data[i]["Description"] = data1[i][4]

            # push_data[i]["Australian Schedule"] = data1[i][3]
            if data1[i][2] is None:
                push_data[i]["Birth"] = "-"
            else:
                push_data[i]["Birth"] = "✔"
                # push_data[i]["Birth"]=data1[i][5]

            if data1[i][3] is None:
                push_data[i]["2 mths"] = "-"
            else:
                push_data[i]["2 mths"] = "✔"
                # push_data[i]["2 mths"] = data1[i][6]
            if data1[i][4] is None:
                push_data[i]["4 mths"] = "-"
            else:
                push_data[i]["4 mths"] = "✔"
                # push_data[i]["4 mths"] = data1[i][7]
            if data1[i][5] is None:
                push_data[i]["6 mths"] = "-"
            else:
                push_data[i]["6 mths"] = "✔"
                # push_data[i]["6 mths"] = data1[i][8]
            if data1[i][6] is None:
                push_data[i]["12 mths"] = "-"
            else:
                push_data[i]["12 mths"] = "✔"
                # push_data[i]["12 mths"] = data1[i][9]
            if data1[i][7] is None:
                push_data[i]["18 mths"] = "-"
            else:
                push_data[i]["18 mths"] = "✔"
                # push_data[i]["18 mths"] = data1[i][10]
            if data1[i][8] is None:
                push_data[i]["2-4 yrs"] = "-"
            else:
                push_data[i]["2-4 yrs"] = "✔"
                # push_data[i]["2-4 yrs"] = data1[i][11]
            if data1[i][9] is None:
                push_data[i][">4 yrs"] = "-"
            else:
                push_data[i][">4 yrs"] = "✔"
                # push_data[i][">4 yrs"] = data1[i][12]
            if data1[i][10] is None:
                push_data[i]["12-18 yrs"] = "-"
            else:
                push_data[i]["12-18 yrs"] = "✔"
                # push_data[i]["12-18 yrs"] = data1[i][13]
            # if data1[i][14] is None:
            #     push_data[i][">18 yrs"]="-"
            # else:
            #     push_data[i][">18 yrs"]=data1[i][14]
            # if data1[i][15] in None:
            #     push_data[i][">24 yrs"]="-"
            # else:
            #     push_data[i][">24 yrs"]=data1[i][15]
            if data1[i][13] is None:
                push_data[i]["pg_w"] = "-"
            else:
                push_data[i]["pg_w"] = "✔"
                # push_data[i]["pg_w"]=data1[i][16]
            if data1[i][14] is None:
                push_data[i][">=60 yrs"] = "-"
            else:
                push_data[i][">=60 yrs"] = "✔"
                # push_data[i][">=60 yrs"]=data1[i][17]
            if data1[i][17] is None:
                 disease_data[i]["Link for vaccine name"] = "-"
            else:
                 disease_data[i]["Link for vaccine name"] = data1[i][17]

            # push_data[i]["Description"] = data1[i][3]
            push_data.append({})
            disease_data.append({})

        out_put = []
        for i in push_data:
            if i != {}:
                out_put.append(i)
        out_put = sorted(out_put, key=lambda e: e['Vaccine Name'], reverse=False)

        out_put2 = []
        for i in disease_data:
            if i != {}:
                out_put2.append(i)
        out_put2 = sorted(out_put2, key=lambda e: e['Vaccine Name'], reverse=False)

    # print(push_data)
    # push_data.sort()
    return render(request, 'au_schedule.html',
                  {'data': json.dumps(list(out_put)), 'disease': json.dumps(list(out_put2))})

def city_council(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    push_data = [{}]
    #if request.method == "POST":
    suburb = request.POST.get("suburb")
    #print(suburb)
    #suburb = request.POST.get('suburb')
    city_council= "select * from suburb_council where suburb = '" + str(suburb) + "'"
    country1 = cur.execute(city_council)
    data1 = country1.fetchall()
        
    if data1:
        for i in range(len(data1)):
            push_data[i]["City council"] = data1[i][3]
            push_data[i]["Phone number"] = data1[i][5]
            push_data[i]["Email address"] = data1[i][7]
            push_data[i]["Website"] = data1[i][8]
            push_data[i]["Address"] = data1[i][4]
                    #push_data[i]["lat"] = data1[i][9]
                    #push_data[i]["lng"] = data1[i][10]
            push_data.append({})
    #print(push_data)
    return render(request, 'city_council.html', {'data': json.dumps(list(push_data)), 
    'explanation': "Please contact your city council to get more information about free vaccinations."})

    

def find_GP(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    language = request.POST.get('language',"Select")
    sentence = "SELECT lat,lng from gp_data where language = '" + str(language) + "'"
    gp_data = cur.execute(sentence).fetchall()

    push_data = [{}]
    if gp_data:
        for i in range(len(gp_data)):
            push_data[i]["lat"] = gp_data[i][0]
            push_data[i]["lng"] = gp_data[i][1]
            push_data.append({})

    return render(request, 'special_GP.html', {'data': json.dumps(list(push_data)), 'language': language})

def check_box(request):
    list = request.POST.getlist('')
    print(list)
    return render(request,"check_box.html")


def free_au_vaccine(request):
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    free_vaccine= "select vaccine_name, Diseases, schedule, link from aus_free_vaccines"
    country1 = cur.execute(free_vaccine)
    data1 = country1.fetchall()
    # data2=country1.fetchall()
    push_data = [{}]
    if data1:
        for i in range(len(data1)):
            push_data[i]["Vaccine Name"] = data1[i][0]
            push_data[i]["Diseases"]=data1[i][1]
            push_data[i]["Schedule"]=data1[i][2]
            push_data[i]["Link"]=data1[i][3]
            push_data.append({})
        out_put = []
        for i in push_data:
            if i != {}:
                out_put.append(i)
        out_put = sorted(out_put, key=lambda e: e['Vaccine Name'], reverse=False)
    return render(request, 'free_au_vaccine.html',
                  {'data': json.dumps(list(out_put))})


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
