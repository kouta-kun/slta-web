import base64
import json
import random
import re
import string
import bcrypt

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
    if request.method == "POST":
        rest_param = json.loads(request.body.decode())
        tok = ("token" in rest_param and rest_param["token"]) or None
        data = {"valid": False}
        if tok is None:
            data['msg'] = 'token is none'
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        elif tok not in toks:
            data['msg'] = 'token is not recognized'
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        vin = ("vin" in rest_param and rest_param["vin"]) or None
        if vin is None:
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        data["valid"] = True
        cname = toks[tok]
        cur.execute(
            'select marca, modelo, anio from vehiculo inner join cliente on cliente.nombre=?'
            'and cliente.idcliente=vehiculo.cliente and vehiculo.vin=?',
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


def get_places(request: HttpRequest):
    global db
    if request.method == "POST":
        rest_param = json.loads(request.body.decode())
        tok = ("token" in rest_param and rest_param["token"]) or None
        data = {"valid": False}
        if tok is None:
            data["msg"] = "No token in request"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        elif tok not in toks:
            data["msg"] = "Token no reconocido, por favor vuelva a conectarse"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        vin = ("vin" in rest_param and rest_param["vin"]) or None
        if vin is None:
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        data["path"] = []
        data["valid"] = True
        cname = toks[tok]
        cur.execute(
            "select l1.geox, l1.geoy, l1.nombre from vehiculo"
            " inner join cliente on vehiculo.cliente=cliente.idcliente"
            " inner join integra on integra.idvehiculo=vehiculo.idvehiculo"
            " inner join lote on integra.lote=lote.idlote and not integra.invalidado"
            " inner join lugar as l1 on l1.idlugar=lote.origen"
            " inner join lugar as l2 on l2.idlugar=lote.destino"
            " where cliente.nombre=? and vehiculo.VIN=?"
            "\nunion\n "
            "select l2.geox, l2.geoy, l2.nombre from vehiculo"
            " inner join cliente on vehiculo.cliente=cliente.idcliente"
            " inner join integra on integra.idvehiculo=vehiculo.idvehiculo"
            " inner join lote on integra.lote=lote.idlote and not integra.invalidado"
            " inner join lugar as l1 on l1.idlugar=lote.origen"
            " inner join lugar as l2 on l2.idlugar=lote.destino"
            " where cliente.nombre=? and vehiculo.VIN=?",
            (cname, vin))
        for r in cur.fetchall():
            data["path"].append({"x": r[1], "y": r[0], "nombre": r[2]})
        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def get_path(request: HttpRequest):
    global db
    if request.method == "POST":
        rest_param = json.loads(request.body.decode())
        tok = ("token" in rest_param and rest_param["token"]) or None
        data = {"valid": False}
        if tok is None:
            data["msg"] = "No token in request"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        elif tok not in toks:
            data["msg"] = "Token no reconocido, por favor vuelva a conectarse"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        vin = ("vin" in rest_param and rest_param["vin"]) or None
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
    if request.method == "POST":
        rest_param = json.loads(request.body.decode())
        tok = ("token" in rest_param and rest_param["token"]) or None
        data = {"valid": False}
        if tok is None:
            data["msg"] = "No token in request"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        elif tok not in toks:
            data["msg"] = "Token no reconocido, por favor vuelva a conectarse"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        car = ("vin" in rest_param and rest_param["vin"]) or None
        if car is None:
            data["msg"] = "No vin in request"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        if db is None:
            opendb()
        data["valid"] = True
        cur: pyodbc.Cursor = db.cursor()
        cur.execute('(select concat(concat('
                    ' usuario.nombredeusuario, ": "),'
                    ' bson_value_varchar(datos, "mensaje"))'
                    ' from evento inner join vehiculo'
                    ' on vehiculo.idvehiculo=bson_value_int(datos,"idvehiculo")'
                    ' inner join usuario on usuario.idusuario=bson_value_int(datos,"autor")'
                    ' and bson_value_varchar(datos, "tipo")="comentario"'
                    ' and bson_value_varchar(datos, "por")="admin"'
                    ' where vin=?'
                    ')'
                    '\nunion all\n'
                    '(select concat(concat('
                    '        cliente.nombre, ": "),'
                    '        bson_value_varchar(datos, "mensaje"))'
                    '  from evento inner join vehiculo'
                    ' on vehiculo.idvehiculo=bson_value_int(datos,"idvehiculo")'
                    ' inner join cliente on cliente.idcliente=bson_value_int(datos,"autor")'
                    ' and bson_value_varchar(datos, "tipo")="comentario"'
                    ' and bson_value_varchar(datos, "por")="cliente"'
                    ' where vin=?'
                    ')', (car, car))
        data["messages"] = []
        for r in cur.fetchall():
            data["messages"].append(r[0])
        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def comment_on(request: HttpRequest):
    global db
    if request.method == "POST":
        rest_param = json.loads(request.body.decode())
        tok = ("token" in rest_param and rest_param["token"]) or None
        data = {"valid": False}
        if tok is None:
            data["msg"] = "No token in request"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        elif tok not in toks:
            data["msg"] = "Token no reconocido, por favor vuelva a conectarse"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        car = ("vin" in rest_param and rest_param["vin"]) or None
        if car is None:
            data["msg"] = "No vin in request"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        msg = ("msg" in rest_param and rest_param["msg"]) or None
        data = {"valid": False}
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        cname = toks[tok]
        msg = base64.b64decode(msg).decode("UTF-8")
        cur.execute("select idcliente from cliente where nombre=?", (cname,))
        authorid = cur.fetchval()
        cur.execute("select idvehiculo from vehiculo where vin=?", (car,))
        vehicleid = cur.fetchval()
        event_json = {
            "tipo": "comentario", "por": "cliente",
            "mensaje": msg, "autor": authorid,
            "idvehiculo": vehicleid
        }
        cur.execute("insert into evento (datos, fechaAgregado) values(?::json, current year to second)",
                    (json.dumps(event_json)))
        if cur.rowcount > 0:
            data["valid"] = True
        return HttpResponse(json.dumps(data), content_type='application/json')


def get_client_data(request: HttpRequest):
    global db
    rest_param = json.loads(request.body.decode())
    tok = ("token" in rest_param and rest_param["token"]) or None
    data = {"valid": False}
    if tok is None:
        data["msg"] = "No token in request"
        return HttpResponse(json.dumps(data), content_type='application/json', status=404)
    elif tok not in toks:
        data["msg"] = "Token no reconocido, por favor vuelva a conectarse"
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
    if request.method == "POST":
        rest_param = json.loads(request.body.decode())
        tok = ("token" in rest_param and rest_param["token"]) or None
        data = {"valid": False}
        if tok is None:
            data["msg"] = "No token in request"
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)
        elif tok not in toks:
            data["msg"] = "Token no reconocido, por favor vuelva a conectarse"
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
            "from vehiculo inner join cliente on vehiculo.cliente=cliente.idcliente "
            " and cliente.nombre=? left join vehiculoIngresa on vehiculoIngresa.idvehiculo=vehiculo.idvehiculo"
            " and vehiculoIngresa.tipoIngreso='Baja'",
            (cname,))
        data['you_are'] = cname
        for r in cur.fetchall():
            data["cars"].append({"vin": r[0], "state": r[1]})
        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


def get_token(request: HttpRequest):
    global db
    if request.method == "POST":
        if db is None:
            opendb()
        cur: pyodbc.Cursor = db.cursor()
        data = {"valid": True, "token": None}
        rest_param = json.loads(request.body.decode())
        cname = ("cname" in rest_param and rest_param["cname"]) or None
        if cname is None:
            data["valid"] = False
            return HttpResponse(json.dumps(data), content_type="application/json", status=404)
        pwd = ("passwd" in rest_param and rest_param["passwd"]) or None
        if pwd is None:
            data["valid"] = False
            return HttpResponse(json.dumps(data), content_type="application/json", status=400)
        cur.execute("select passphrase from cliente where nombre=?", (cname,))
        passphrase: str = cur.fetchval()
        if passphrase is None:
            defpwd = (str(cname) + "-change!").encode()
            hashed = bcrypt.hashpw(defpwd, bcrypt.gensalt())
            if type(hashed) != str:
                hashed = hashed.decode()
            cur.execute("update cliente set passphrase=? where nombre=?", (hashed, cname))
            cur.execute("select passphrase from cliente where nombre=?", (cname,))
            passphrase: str = cur.fetchval()
        passphrase_bytes = passphrase.encode()
        pwd_bytes = passphrase.encode()
        if bcrypt.checkpw(pwd_bytes, passphrase_bytes):
            tkn = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=12))
            toks[tkn] = cname
            data["token"] = tkn
            return HttpResponse(json.dumps(data), content_type="application/json", status=200)
        else:
            data["valid"] = False
            return HttpResponse(json.dumps(data), content_type="application/json", status=404)
