import requests
import json
import pymysql

def insertarEnInvoices(sentenciaSQL):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","Invoices" )
    cursor = db.cursor()
    
    rowsCount=cursor.execute(sentenciaSQL)
    
    idInserted=cursor.lastrowid;
    
    db.commit()      
    db.close()
    
    return idInserted

#catEntradas;
#+---------------+--------------+------+-----+---------+----------------+
#| Field         | Type         | Null | Key | Default | Extra          |
#+---------------+--------------+------+-----+---------+----------------+
#| iidEntrada    | int(11)      | NO   | PRI | NULL    | auto_increment |
#| ccodigo       | varchar(64)  | YES  |     | NULL    |                |
#| dtfecha       | datetime     | YES  |     | NULL    |                |
#| cdescripcion  | varchar(255) | YES  |     | NULL    |                |
#| icantidad     | float        | YES  |     | NULL    |                |
#| iimporte      | float        | YES  |     | 0       |                |
#| clogin        | varchar(50)  | YES  |     | NULL    |                |
#| entrada       | int(1)       | YES  |     | NULL    |                |
#| observaciones | varchar(255) | YES  |     | NULL    |                |
#| idAlmacen     | int(11)      | YES  |     | NULL    |                |
#+---------------+--------------+------+-----+---------+----------------+
def insertarCatEntradas(codigoProd, descrip, cantidad, precio):
    # MySQL Server credentials

    qry = "INSERT INTO catEntradas(ccodigo,dtfecha,cdescripcion,icantidad,iimporte,clogin,entrada,observaciones,idAlmacen) VALUES('{0}',NOW(),'{1}',{2},{3},'script',0,'Insercion automatizada',1)".format(codigoProd, descrip, cantidad, precio)

    print(qry)
    
    insertarEnInvoices(qry)
    
#catPedidosWeb;
#+---------------+--------------+------+-----+---------+----------------+
#| Field         | Type         | Null | Key | Default | Extra          |
#+---------------+--------------+------+-----+---------+----------------+
#| idPedidoWeb   | int(11)      | NO   | PRI | NULL    | auto_increment |
#| idAlmacenOrig | int(11)      | NO   |     | NULL    |                |
#| Fecha         | datetime     | NO   |     | NULL    |                |
#| Observaciones | varchar(255) | NO   |     |         |                |
#| usuario       | varchar(50)  | YES  |     | NULL    |                |
#+---------------+--------------+------+-----+---------+----------------+
def insertarCatPedidoWeb():

    qry = "INSERT INTO catPedidosWeb(idAlmacenOrig, Fecha, Observaciones, usuario) VALUES(1, NOW(), 'Insercion automatizada', 'script')"

    print(qry)
    
    return insertarEnInvoices(qry)
    
#detPedidosWeb;
#+----------------+---------+------+-----+---------+----------------+
#| Field          | Type    | Null | Key | Default | Extra          |
#+----------------+---------+------+-----+---------+----------------+
#| idDetPedidoWeb | int(11) | NO   | PRI | NULL    | auto_increment |
#| idPedidoWeb    | int(11) | NO   |     | NULL    |                |
#| idProducto     | int(11) | NO   |     | NULL    |                |
#| Cantidad       | float   | NO   |     | NULL    |                |
#| idAlmacenDest  | int(11) | NO   |     | NULL    |                |
#| Solicitado     | float   | YES  |     | 0       |                |
#| Estado         | char(1) | YES  |     | NULL    |                |
#+----------------+---------+------+-----+---------+----------------+
def insertarDetPedidoWeb(idPedidoWeb, idProducto, Cantidad, idAlmacenDest):

    qry = "INSERT INTO detPedidosWeb(idPedidoWeb, idProducto, Cantidad, idAlmacenDest, Solicitado, Estado) VALUES({0}, {1}, {2}, {3}, {4}, 1)".format(idPedidoWeb, idProducto, Cantidad, idAlmacenDest, Cantidad)

    print(qry)
    
    insertarEnInvoices(qry)

if __name__ == '__main__':

    r = requests.get('http://0.0.0.0:5001/pedidos/')
    jsonResponse = r.json()

    currPedido=-1
    if jsonResponse["isError"] == False:
        #print("No es error!")
        for campoValor in jsonResponse["result"]:
            if currPedido != campoValor["idPedido"]:
                if currPedido != -1:
                    #Cerrar el pedido!
                    print("Cerrar el pedido {0}".format(currPedido))
                    cerrarPedido="http://0.0.0.0:5001/pedidos/{0}".format(campoValor["idPedido"])
                    r = requests.get(cerrarPedido)
                    jsonResponse = r.json()
                    print(jsonResponse)
                    
                currPedido = campoValor["idPedido"]
                print("*************** Pedido {0} *******************".format(campoValor["idPedido"]))
                #Procesamos un nuevo pedido
                idPedido=insertarCatPedidoWeb()
        
            print("idProducto = {0}, idLocacion={1}, iCantidad={2}".format(campoValor["idProducto"],campoValor["idLocacion"],campoValor["iCantidad"]))
            insertarDetPedidoWeb(idPedido, campoValor["idProducto"], campoValor["iCantidad"], campoValor["idLocacion"])
            insertarCatEntradas(campoValor["CodigoProd"], campoValor["Descripcion"], campoValor["iCantidad"]*-1, campoValor["PrecioalCliente"])
        
        if currPedido != -1:
            #Cerrar el pedido!
            print("Cerrar el pedido* {0}".format(currPedido))
            cerrarPedido2="http://0.0.0.0:5001/pedidos/{0}".format(campoValor["idPedido"])
            r = requests.get(cerrarPedido2)
            jsonResponse2 = r.json()
            print(jsonResponse2)

