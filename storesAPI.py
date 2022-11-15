#!flask/bin/python
# IPC
#
# Miguel Mota Jun 2021
#
# API para la sincronizaciÃn de productos
#
from flask import Flask, request, jsonify
from flask import abort
from waitress import serve
import pymysql
import json
import redis
from datetime import datetime
from datetime import timedelta, date

#iptables -I INPUT -p tcp -s 0.0.0.0/0 --dport 5002 -j ACCEPT
#waitress-serve --call 'storesAPI:create_app' &

app = Flask(__name__)

# *************  Generic functions ***************

# Regresa un producto por codigo
# Miguel Mota Jul 27 2020
#
@app.route("/productos/<claveTienda>", methods=['GET'])
def productoPorCodigo(claveTienda):

    r = redis.Redis(host='localhost', port=6379, db=0)

    idsFechas = json.loads(r.get("idsFechas"))

    lClaveTienda = ("T"+claveTienda)

    if r.get(lClaveTienda) == None:
        #print("La tienda no esta en la base de datos...")
        ultimaActualizacion_="2021-01-01 00:00:00"
    else:
        #print("La tienda ya esta en la base de datos :")
        ultimaActualizacion=r.get(lClaveTienda)
        ultimaActualizacion_=ultimaActualizacion.decode("utf-8")
        
    #print(ultimaActualizacion_)
    fechaUltimaAct = datetime.strptime(ultimaActualizacion_, '%Y-%m-%d %H:%M:%S')

    productosParaActalizar = []
    for prodItem in idsFechas:
        fechaModificado = datetime.strptime(prodItem["fechaModificado"], '%Y-%m-%d %H:%M:%S')

        if fechaModificado > fechaUltimaAct:
            productosParaActalizar.append(json.loads(r.get(prodItem["id"])))

    return json.dumps(productosParaActalizar)

@app.route("/productos/actualizacion/<claveTienda>/<fechaUltAct>", methods=['GET'])
def productoActualizacion(claveTienda, fechaUltAct):

    r = redis.Redis(host='localhost', port=6379, db=0)

    #x = datetime.now()
    #fechaUltAct = "{0}-{1}-{2} {3}:{4}:{5}".format(x.strftime("%Y"), x.strftime("%m"), x.strftime("%d"), x.strftime("%H"), x.strftime("%M"), x.strftime("%S"))

    lClaveTienda = ("T"+claveTienda)

    #fechaUltAct="2021-01-01 00:00:00"
    r.set(lClaveTienda, fechaUltAct.encode("utf-8"))

    return jsonify(isError=False, statusCode=200) 

def create_app():
    serve(app, host='0.0.0.0', port=5002)

if __name__ == '__main__':
    print(__name__)
    serve(app, host='0.0.0.0', port=5002)
