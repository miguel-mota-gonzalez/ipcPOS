import requests
import json
import pymysql
#import datetime
from datetime import datetime
from datetime import timedelta, date

def getColumnNames(tableName):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","Invoices")
    cursor = db.cursor()

    lQuery = "describe {0};".format(tableName)

    rowsCount=cursor.execute(lQuery)

    returnData = []
    for data in cursor.fetchall():
        returnData.append(data[0])

    db.close()

    #print(returnData)

    return returnData

def obtenerIdLocal(idGlobal):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","Invoices")
    cursor = db.cursor()

    lQuery = "select idLocal from catArticulosNube where  idNube = {0}".format(idGlobal)

    #print(lQuery)

    rowsCount=cursor.execute(lQuery)

    returnData = []
    for data in cursor.fetchall():
        returnData.append(data[0])

    db.close()

    #print(returnData)

    return returnData


def actualizarRegistro(querySQL, params):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","Invoices" )
    cursor = db.cursor()

    rowsCount=cursor.execute(querySQL, params)

    db.commit()
    db.close()

    print("Registros actualizados {0}".format(rowsCount))

    return rowsCount

def insertarRegistro(sentenciaSQL, params):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","Invoices" )
    cursor = db.cursor()

    rowsCount=cursor.execute(sentenciaSQL, params)

    idInserted=cursor.lastrowid

    db.commit()
    db.close()

    return idInserted


#mysql> describe catArticulosNube;
#+-----------------+----------+------+-----+---------+-------+
#| Field           | Type     | Null | Key | Default | Extra |
#+-----------------+----------+------+-----+---------+-------+
#| idNube          | int(11)  | NO   | PRI | NULL    |       |
#| idLocal         | int(11)  | NO   | PRI | NULL    |       |
#| dtFechaAct      | datetime | NO   |     | NULL    |       |
#| dtFechaDownload | datetime | NO   |     | NULL    |       |
#+-----------------+----------+------+-----+---------+-------+
#4 rows in set (0.00 sec)

if __name__ == '__main__':

    with open('prodConf.json') as json_file:
        confProd = json.load(json_file)

    idTienda=confProd["idTienda"]

    x = datetime.now()
    nombreLog = "./{0}_{1}_{2}_{3}_{4}_{5}.log".format(x.strftime("%Y"), x.strftime("%m"), x.strftime("%d"), x.strftime("%H"), x.strftime("%M"), x.strftime("%S"))
  
    print(nombreLog)
    fp = open(nombreLog, 'w')

    colNames = getColumnNames('catProductos')

    r = requests.get('http://45.55.248.209:5002/productos/{0}'.format(idTienda))
    jsonResponse = r.json()

    totalReg=0
    wentOK = True
    dtRegModificado = datetime.strptime("2021-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    for producto in jsonResponse:
        totalReg = totalReg + 1
        primero = True
        updateSQL = "update catProductos SET ";
        insertSQL = "insert into catProductos("
        insertVSQL = " values("
        prodData = []

        if datetime.strptime(producto["dtRegModificado"], '%Y-%m-%d %H:%M:%S') > dtRegModificado:
            dtRegModificado = datetime.strptime(producto["dtRegModificado"], '%Y-%m-%d %H:%M:%S') 

        for colN in colNames:

            if colN!="IdProducto":

                if primero==False:
                    updateSQL = (updateSQL + ",")
                    insertSQL = (insertSQL + ",")
                    insertVSQL = (insertVSQL + ",")

                primero=False

                updateSQL = updateSQL + colN + " = %s"
                insertSQL = insertSQL + colN
                insertVSQL = insertVSQL + "%s"
 
                value = producto[colN]
                if str(type(value))=="<class 'str'>":
                    prodData.append(value.encode('ascii', 'ignore').decode('ascii'))
                else:
                    prodData.append(value)

        idProdArr = obtenerIdLocal(producto["IdProducto"])
        if len(idProdArr) > 0:
            print("Actualizar {0}...".format(idProdArr[0]))
            fp.write("Actualizar {0}...\n".format(idProdArr[0]))
            prodData.append(idProdArr[0])
            updateSQL = updateSQL + " where idProducto = %s;"
            #print(updateSQL)
            if actualizarRegistro(updateSQL, prodData) < 1:
                print("No se actualizo")
                fp.write("No se actualizo\n")
                #wentOK=False
        else:
            print("Insertar {0}...".format(producto["IdProducto"]))
            fp.write("Insertar {0}...\n".format(producto["IdProducto"]))
            insertSQL = insertSQL + ") " + insertVSQL + ");";
            #print(insertSQL)
            nuevoId=insertarRegistro(insertSQL, prodData)
            insertNubeRef="insert into catArticulosNube(idNube, idLocal, dtFechaAct, dtFechaDownload) values(%s, %s, NOW(), NOW());";
            paramsNube = []
            paramsNube.append(producto["IdProducto"]) 
            paramsNube.append(nuevoId)
            fp.write("nuevo id {0}".format(nuevoId))
            print("nuevo id {0}\n".format(nuevoId))
            if actualizarRegistro(insertNubeRef, paramsNube) < 1:
                print("No se inserto")
                fp.write("No se inserto\n")
                wentOK=False

    if wentOK == True:
        print("Actualuzacion completada exitosamene...")
        fp.write("Actualizacion completada exitosamente\n")
        if totalReg > 0:
            print(dtRegModificado)
            resultEnd=requests.get('http://45.55.248.209:5002/productos/actualizacion/{0}/{1}'.format(idTienda,dtRegModificado))
            print('http://45.55.248.209:5002/productos/actualizacion/{0}/{1}'.format(idTienda,dtRegModificado))
            print(resultEnd)
    else:
        print("Actualuzacion completada con errores...")
        fp.write("Actualizacion completada con errores\n")

    fp.close()
