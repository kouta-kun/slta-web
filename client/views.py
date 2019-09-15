import base64
import json
import random
import re
import string

from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import render
import pyodbc

db = None
toks = {}


def index(request: HttpRequest):
    global db
    if request.method == "GET":
        template = loader.get_template("client/index.html")
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


def get_status(request: HttpRequest):
    global db
    if request.method == "GET":
        tok = request.GET.get("token", None)
        data = {"valid": False}
        if tok is None or tok not in toks.keys():
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        vin = request.GET.get("vin", None)
        if vin is None:
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        data["valid"] = True
        cname = toks[tok]
        cur.execute(
            'select marca, modelo, anio from vehiculo inner join cliente on cliente.nombre=? and cliente.idcliente=vehiculo.cliente and vehiculo.vin=?',
            (cname, vin))
        r = cur.fetchone()
        data["marca"] = r[0]
        data["modelo"] = r[1]
        data["anio"] = r[2]
        return HttpResponse(json.dumps(data), content_type='application/json')


uruguay_left_bound = (-33.598051, -58.491343)[1]
uruguay_top_bound = (-30.085503, -57.068193)[0]
uruguay_right_bound = (-32.735860, -53.082159)[1]
uruguay_bottom_bound = (-34.973293, -54.951898)[0]


def get_gridpath(request: HttpRequest):
    global db
    if request.method == "GET":
        tok = request.GET.get("token", None)
        data = {"valid": False}
        if tok is None or tok not in toks.keys():
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        vin = request.GET.get("vin", None)
        if vin is None:
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        data["path"] = []
        data["valid"] = True
        cname = toks[tok]
        cur.execute(
            "select l1.geox, l1.geoy, l2.geox, l2.geoy, l1.tipo, l2.tipo, l1.nombre, l2.nombre from vehiculo"
            " inner join cliente on vehiculo.cliente=cliente.idcliente"
            " inner join integra on integra.idvehiculo=vehiculo.idvehiculo"
            " inner join lote on integra.lote=lote.idlote and not integra.invalidado"
            " inner join lugar as l1 on l1.idlugar=lote.origen"
            " inner join lugar as l2 on l2.idlugar=lote.destino"
            " where cliente.nombre=? and vehiculo.VIN=?",
            (cname, vin))
        for r in cur.fetchall():
            relX_1 = (abs(uruguay_left_bound - r[1]) / abs(uruguay_left_bound - uruguay_right_bound))
            relX_1 = relX_1*32 + 2

            relY_1 = (abs(uruguay_top_bound - r[0]) / abs(uruguay_top_bound - uruguay_bottom_bound))
            relY_1 = relY_1*29 + 3

            relX_2 = (abs(uruguay_left_bound - r[3]))
            relX_2 = relX_2 / abs(uruguay_left_bound - uruguay_right_bound)
            relX_2 = relX_2*32 + 2

            relY_2 = (abs(uruguay_top_bound - r[2]) / abs(uruguay_top_bound - uruguay_bottom_bound))
            relY_2 = relY_2*29 + 3

            data["path"].append((int(relX_1), int(relY_1)-1, r[4], r[6]))
            data["path"].append((int(relX_2), int(relY_2)-1, r[5], r[7]))
        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def get_path(request: HttpRequest):
    global db
    if request.method == "GET":
        tok = request.GET.get("token", None)
        data = {"valid": False}
        if tok is None or tok not in toks.keys():
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        vin = request.GET.get("vin", None)
        if vin is None:
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        data["path"] = []
        data["valid"] = True
        cname = toks[tok]
        cur.execute(
            "select concat(concat(l1.nombre, '-'), l2.nombre) from vehiculo"
            " inner join cliente on vehiculo.cliente=cliente.idcliente"
            " inner join integra on integra.idvehiculo=vehiculo.idvehiculo"
            " inner join lote on integra.lote=lote.idlote and not integra.invalidado"
            " inner join lugar as l1 on l1.idlugar=lote.origen"
            " inner join lugar as l2 on l2.idlugar=lote.destino"
            " where cliente.nombre=? and vehiculo.VIN=?",
            (cname, vin))
        print(cname)
        print(vin)
        for r in cur.fetchall():
            data["path"].append(r[0])
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def comments_for(request: HttpRequest):
    global db
    if request.method == "GET":
        tok = request.GET.get("token", None)
        car = request.GET.get("vin", None)
        data = {"valid": False}
        if tok is None or tok not in toks.keys() or car is None:
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        data["valid"] = True
        cur: pyodbc.Cursor = db.cursor()
        cur.execute("select concat(concat(concat('Cliente: ', comentario), ' @ '), fecha), fecha"
                    " from comentarioCliente "
                    "inner join vehiculo on comentarioCliente.idvehiculo=vehiculo.idvehiculo where VIN=?\nunion\n"
                    "select concat(concat(concat('Administrativo: ', comentario), ' @ '), fecha), fecha"
                    " from comentarioUsuario "
                    "inner join vehiculo on comentarioUsuario.idvehiculo=vehiculo.idvehiculo where VIN=?"
                    " order by 2;", (car, car))
        data["messages"] = []
        for r in cur.fetchall():
            data["messages"].append(r[0])
        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def comment_on(request: HttpRequest):
    global db
    if request.method == "GET":
        tok = request.GET.get("token", None)
        car = request.GET.get("vin", None)
        msg = request.GET.get("msg", None)
        data = {"valid": False}
        if tok is None or tok not in toks.keys() or car is None or msg is None:
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        cname = toks[tok]
        msg = base64.b64decode(msg).decode("UTF-8")
        kupdate = re.search("es un ([A-Z][a-z]+) ([0-9A-Za-z]+) del ([0-9]{4})", msg)
        print(kupdate)
        print(msg)
        if kupdate:
            cur.execute("update vehiculo set marca=?, modelo=?, anio=? where vin=?",
                        (kupdate.group(1), kupdate.group(2), int(kupdate.group(3)), car))
        cur.execute("insert into comentariocliente values((select idvehiculo from vehiculo where VIN=?), "
                    "(select idcliente from cliente where nombre=?), current year to second, ?);", (car, cname, msg))
        if cur.rowcount > 0:
            data["valid"] = True
        return HttpResponse(json.dumps(data), content_type='application/json')


def get_client_data(request: HttpRequest):
    global db
    tok = request.GET.get("token", None)
    data = {"valid": False}
    if tok is None or tok not in toks.keys():
        return HttpResponse(json.dumps(data), content_type='application/json', status=404)
    if db is None:
        opendb()
    cur: pyodbc.Cursor = db.cursor()
    data["valid"] = True
    cname = toks[tok]
    data["nombre"] = cname
    cur.execute("select rut from cliente where nombre=?", (cname,))
    data["rut"] = cur.fetchval()
    return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def get_cars(request: HttpRequest):
    global db
    if request.method == "GET":
        tok = request.GET.get("token", None)
        data = {"valid": False}
        if tok is None or tok not in toks.keys():
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        data["cars"] = []
        data["valid"] = True
        cname = toks[tok]
        cur.execute(
            "select VIN, case"
            " when vehiculoIngresa.idvehiculo is null then 1"
            " else 0"
            " end as active "
            "from vehiculo left join vehiculoIngresa on vehiculoIngresa.idvehiculo=vehiculo.idvehiculo and vehiculoIngresa.tipoIngreso='Baja' inner join cliente on vehiculo.cliente=cliente.idcliente and cliente.nombre=?",
            (cname,))
        for r in cur.fetchall():
            data["cars"].append({"vin": r[0], "state": r[1]})
        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def get_token(request: HttpRequest):
    global db
    if request.method == "GET":
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        data = {"valid": True, "token": None}
        cname = request.GET.get("cname", None)
        if cname is None:
            data["valid"] = False
            return HttpResponse(json.dumps(data), content_type="application/json", status=404)
        pwd = request.GET.get("passwd", None)
        if pwd is None:
            data["valid"] = False
            return HttpResponse(json.dumps(data), content_type="application/json", status=400)
        cur.execute("select count(*) from cliente where nombre=? and pin=?", (cname, pwd))
        rowcount = cur.fetchval()
        if rowcount > 0:
            tkn = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=12))
            toks[tkn] = cname
            data["token"] = tkn
            return HttpResponse(json.dumps(data), content_type="application/json", status=200)
        else:
            data["valid"] = False
            return HttpResponse(json.dumps(data), content_type="application/json", status=404)
