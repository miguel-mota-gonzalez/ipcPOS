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


def ejecutarSentencia(querySQL, params):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","Invoices" )
    cursor = db.cursor()

    rowsCount=cursor.execute(querySQL, params)

    db.commit()
    db.close()

    print("Registros afectados {0}".format(rowsCount))

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


#mysql> describe catProveedores;
#+-------------+--------------+------+-----+---------+----------------+
#| Field       | Type         | Null | Key | Default | Extra          |
#+-------------+--------------+------+-----+---------+----------------+
#| IdProveedor | int(11)      | NO   | PRI | NULL    | auto_increment |
#| Nombre      | varchar(255) | YES  |     | NULL    |                |
#| Direccion   | text         | YES  |     | NULL    |                |
#| Fax         | varchar(50)  | YES  |     | NULL    |                |
#| Telefono    | varchar(50)  | YES  |     | NULL    |                |
#| RFC         | varchar(50)  | YES  |     | NULL    |                |
#| Fecha       | datetime     | YES  |     | NULL    |                |
#| email       | varchar(50)  | YES  |     | NULL    |                |
#| contacto    | text         | YES  |     | NULL    |                |
#| ciudad      | varchar(50)  | YES  |     | NULL    |                |
#+-------------+--------------+------+-----+---------+----------------+
#10 rows in set (0.00 sec)

if __name__ == '__main__':

    x = datetime.now()
    nombreLog = "./prov_{0}_{1}_{2}_{3}_{4}_{5}.log".format(x.strftime("%Y"), x.strftime("%m"), x.strftime("%d"), x.strftime("%H"), x.strftime("%M"), x.strftime("%S"))
  
    print(nombreLog)
    fp = open(nombreLog, 'w')

    colNames = getColumnNames('catProveedores_')
    print(colNames)

    r = requests.get('http://server:5001/proveedores/')
    jsonResponse = r.json()

    #print(jsonResponse)

    pd = []
    ejecutarSentencia("DELETE FROM catProveedores_;", pd)

    totalReg=0
    wentOK = True
    dtRegModificado = datetime.strptime("2021-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    for producto in jsonResponse["result"]:
        totalReg = totalReg + 1
        primero = True
        #updateSQL = "update catProductos SET ";
        insertSQL = "insert into catProveedores_("
        insertVSQL = " values("
        prodData = []

        for colN in colNames:

            if primero==False:
                insertSQL = (insertSQL + ",")
                insertVSQL = (insertVSQL + ",")

            primero=False

            insertSQL = insertSQL + colN
            insertVSQL = insertVSQL + "%s"
 
            value = producto[colN]
            if str(type(value))=="<class 'str'>":
                prodData.append(value.encode('ascii', 'ignore').decode('ascii'))
            else:
                prodData.append(value)

        print("Insertar {0}...".format(producto["IdProveedor"]))
        fp.write("Insertar {0}...\n".format(producto["IdProveedor"]))
        insertSQL = insertSQL + ") " + insertVSQL + ");";
        print(insertSQL)
        print (prodData)
        nuevoId=insertarRegistro(insertSQL, prodData)
        print("Insertado...")

    fp.close()
