#!flask/bin/python
# mypos API
#
# Miguel Mota Jul 2020
#
#
from flask import Flask, request, jsonify
from flask import abort
from waitress import serve
import pymysql
import json

#iptables -I INPUT -p tcp -s 0.0.0.0/0 --dport 5001 -j ACCEPT
#waitress-serve --call 'myposapi:create_app' &

print("Start!")

app = Flask(__name__)

# *************  Generic functions ***************

def getColumnNames(tableName):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "describe {0};".format(tableName)
    
    rowsCount=cursor.execute(lQuery)
    
    returnData = []
    for data in cursor.fetchall():
        returnData.append(data[0])

    db.close()
    
    #print(returnData)

    return returnData

# ************* API's   ***************

# Regresa una lista de proveedores
# Miguel Mota Oct 23 2021
#
@app.route("/proveedores/", methods=['GET'])
def proveedores():

    colNames = getColumnNames('catProveedores')

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "select * from catProveedores;"
    
    rowsCount=cursor.execute(lQuery)
    
    rows = []
    for data in cursor.fetchall():
        returnDataItem = {}
        colIndex = 0        
        for item in data:
            returnDataItem[colNames[colIndex]]=item
            colIndex = colIndex + 1
        rows.append(returnDataItem)

    db.close()

    return jsonify(isError=False, result=rows, statusCode=200)

# Regresa una lista de productos
# Miguel Mota Jul 27 2020
#
@app.route("/productos/", methods=['GET'])
def productos():

    colNames = getColumnNames('catProductos')

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "select * from catProductos;"
    
    rowsCount=cursor.execute(lQuery)
    
    rows = []
    for data in cursor.fetchall():
        returnDataItem = {}
        colIndex = 0        
        for item in data:
            returnDataItem[colNames[colIndex]]=item
            colIndex = colIndex + 1
        rows.append(returnDataItem)

    db.close()

    return jsonify(isError=False, result=rows, statusCode=200)
    
# Regresa un producto por codigo
# Miguel Mota Jul 27 2020
#
@app.route("/productos/<codigoProd>", methods=['GET'])
def productoPorCodigo(codigoProd):

    colNames = getColumnNames('catProductos')

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "select * from catProductos where CodigoProd = '{0}';".format(codigoProd)
    
    rowsCount=cursor.execute(lQuery)
    
    returnData = {}
    for data in cursor.fetchall():
        colIndex = 0        
        for item in data:
            returnData[colNames[colIndex]]=item
            colIndex = colIndex + 1
            
    db.close()

    return jsonify(isError=False, result=returnData, statusCode=200)
    
# Regresa un pedidos pendientes
# Miguel Mota Oct 1 2020
#
@app.route("/pedidos/", methods=['GET'])
def pedidos():

    #colNames = getColumnNames('catProductos')
    #  idPedido | idLocacion | idProducto | iCantidad
    colNames = []
    colNames.append("idPedido")
    colNames.append("idLocacion")
    colNames.append("CodigoProd")
    colNames.append("Descripcion")
    colNames.append("PrecioalCliente")
    colNames.append("idProducto")
    colNames.append("iCantidad")

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "select cp.idPedido, cp.idLocacion, ca.CodigoProd, ca.Descripcion, ca.PrecioalCliente, dp.idProducto, dp.iCantidad from catPedido cp inner join detPedido dp on cp.idPedido=dp.idPedido inner join catProductos ca on dp.idProducto = ca.idProducto where cp.iStatus = 1 order by cp.idPedido, cp.idLocacion, dp.idProducto;"
    
    rowsCount=cursor.execute(lQuery)
    
    rows = []
    for data in cursor.fetchall():
        returnData = {}
        colIndex = 0        
        for item in data:
            returnData[colNames[colIndex]]=item
            colIndex = colIndex + 1
        rows.append(returnData)
            
    db.close()

    return jsonify(isError=False, result=rows, statusCode=200)
    
# Actualiza el estado de un pedido
# Miguel Mota Oct 1 2020
#
@app.route("/pedidos/<idPedido>", methods=['GET'])
def marcarComoProcesado(idPedido):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "update catPedido set iStatus=3 where idPedido = {0};".format(idPedido)
    
    rowsCount=cursor.execute(lQuery)
    
    db.commit()      
    db.close()

    return jsonify(isError=False, updated=rowsCount, statusCode=200)
    
# Regresa un pedido a pendiente porque ningun producto tiene existencia
# Miguel Mota Oct 13 2020
#
@app.route("/pedidos/error/<idPedido>", methods=['GET'])
def marcarPedidoComoInsuficiente(idPedido):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "update catPedido set iStatus=0 where idPedido = {0};".format(idPedido)
    
    rowsCount=cursor.execute(lQuery)
    
    db.commit()      
    db.close()

    return jsonify(isError=False, updated=rowsCount, statusCode=200)
    
# Inserta un producto en la lista de no procesados
# Miguel Mota Oct 1 2020
#
@app.route("/pedidos/error/<idPedido>/<idProducto>", methods=['GET'])
def marcarComoInsuficiente(idPedido, idProducto):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    #lQuery = "update catPedido set iStatus=0 where idPedido = {0};".format(idPedido)
    
    
    #describe catNoProcesados;
    #+--------------+-------------+------+-----+---------+-------+
    #| Field        | Type        | Null | Key | Default | Extra |
    #+--------------+-------------+------+-----+---------+-------+
    #| idPedido     | int(11)     | NO   | PRI | NULL    |       |
    #| idProducto   | int(11)     | NO   | PRI | NULL    |       |
    #| iCantidad    | int(11)     | YES  |     | NULL    |       |
    #| sDescripcion | varchar(50) | YES  |     | NULL    |       |
    #| dtFecha      | datetime    | YES  |     | NULL    |       |
    #+--------------+-------------+------+-----+---------+-------+
    
    lQueryInsert = "insert into catNoProcesados(idPedido,idProducto,iCantidad,sDescripcion,dtFecha) values({0},{1},0,'Existencia insuficiente.',NOW());".format(idPedido,idProducto)
    
    #rowsCount=cursor.execute(lQuery)
    
    rowsCount=cursor.execute(lQueryInsert)
    
    db.commit()      
    db.close()

    return jsonify(isError=False, updated=rowsCount, statusCode=200)
    
# Actualiza el estado de un pedido
# Miguel Mota Oct 1 2020
#
@app.route("/pedidos/<idPedido>/<idProducto>/<iCantidad>", methods=['GET'])
def actualizarCantidadSurtida(idPedido, idProducto, iCantidad):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "update detPedido set iCantidadSurtida={0} where idPedido = {1} AND idProducto = {2};".format(iCantidad, idPedido, idProducto)
    
    rowsCount=cursor.execute(lQuery)
    
    db.commit()      
    db.close()

    return jsonify(isError=False, updated=rowsCount, statusCode=200)

# Inserta un registro de totales
# Miguel Mota Oct 1 2020
#
@app.route("/totales/<idTienda>/<idTotal>/<cajero>/", methods=['POST'])
def insertarTotal(idTienda, idTotal, cajero):

    content = request.json

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    lQuery = "INSERT INTO detTotalPorDia(idLocacion,idTotal,dtFecha,cCajero,dTotal,dTotal2,dtFechaAlta,dtFechaAct) values({0}, {1}, NOW(), '{2}', {3}, {4}, NOW(), NOW());".format(idTienda, idTotal, cajero, content["total1"], content["total2"])
    rowsCount=cursor.execute(lQuery)
    
    db.commit()      
    db.close()

    return jsonify(isError=False, updated=rowsCount, statusCode=200, qry=lQuery)

# Insertar un registro de totales
# Miguel Mota Ago 13 2021
#
@app.route("/totales/v2/<idTienda>/<idTotal>/<cajero>/", methods=['POST'])
def insertarTotal2(idTienda, idTotal, cajero):

    content = request.json

    #print(content)

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()

    lQuery = "INSERT INTO detTotalPorDia(idLocacion,idTotal,dtFecha,cCajero,dTotal,dTotal2,dtFechaAlta,dtFechaAct) values({0}, {1}, '{5}', '{2}', {3}, {4}, NOW(), NOW());".format(idTienda, idTotal, cajero, content["total1"], content["total2"], content["fecha"])
    rowsCount=cursor.execute(lQuery)
    
    db.commit()      
    db.close()

    return jsonify(isError=False, updated=rowsCount, statusCode=200, qry=lQuery)

def create_app():
    serve(app, host='45.55.248.209', port=5001)

if __name__ == '__main__':
    print(__name__)
    serve(app, host='45.55.248.209', port=5001)
