import pyodbc
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

db = None
toks = {}


def index(request: HttpRequest):
    global db
    if request.method == "GET":
        template = loader.get_template("public/index.html")
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        cur.execute("select count(*) from cliente")
        clients = cur.fetchval()
        cur.execute("select count(*) from vehiculo")
        cars = cur.fetchval()
        cur.execute("select count(*) from lote")
        lotes = cur.fetchval()
        ctx = {"cl_target": clients, "ca_target": cars, "lc_target": lotes}
        return HttpResponse(template.render(ctx, request))


def opendb():
    global db
    db = pyodbc.connect('DRIVER={IBM INFORMIX ODBC DRIVER (64-bit)};DATABASE=bitinfo' +
                        ';SERVER=ol_esi;HOST=192.168.0.121;Service=9088;UID=root;PWD=root;')
