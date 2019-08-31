from django.shortcuts import render
from django.views.generic import ListView
from .models import Post
from django.http import HttpResponse
import sqlite3
from sqlite3 import Error
import os
import json
import pandas as pd 
import dash 
import dash_table

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

def index(request):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    database = os.path.join(BASE_DIR, '6.db')
    conn = create_connection(database)
    cur = conn.cursor()
    country_name = request.POST.get('country',False)
    excute_sentence = "SELECT country_name, schedule, vaccine_code, vaccine_desc from VaccineInfoSet where country_name = '" + str(country_name) + "'"
    cur.execute(excute_sentence)
    rows = cur.fetchall()
    # with conn:
    #     # print("1. Query task by priority:")
    #     # select_task_by_priority(conn, 1)
    #     test = select_all_tasks(conn)
    return render(request,'advanced_search.html',{'data':json.dumps(list(rows))})  # using json.dumps to push the data, using render to pass the content to htmlfile

def Australia_vaccine(request):
    database = os.path.join(BASE_DIR, '6.db')
    #database = r".\db.db"
    conn =  create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT vaccine_code, schedule, vaccine_desc from VaccineInfoSet where country_name = 'Australia'")
    title = cur.fetchall()
    #print(type(title[0]))
    new_1= []
    print("THIS IS")
    for i in title:
        new_1.append(list(i))
    #new_1='\n'.join(str(new_1))
    new_2 = pd.DataFrame(new_1, columns=['Vaccine name', 'Schedule', 'Dscription'])
    print(new_2)
    app = dash.Dash(__name__)
    app.layout = dash_table.DataTable(
        id = 'table',
        columns= [{"name":i, "id":i} for i in new_2],
        data = new_2.to_dict('records')
    )
    print(app.layout)


    #title_d = { i : new_1[i] for i in range(0, len(new_1) ) }
    #print(title_d)
    #print(rows[0][0])
    # for row in rows:
    #     print(row)
    #return rows
    #return HttpResponse(title)
    #return render(request,'quick_search.html',{'data':json.dumps(title_d)})
    return render(request,'quick_search.html',{'data':new_2})
    #return render(request,'quick_search.html', rows)



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