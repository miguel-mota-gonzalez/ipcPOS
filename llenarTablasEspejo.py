import requests
import json
import pymysql
#import datetime
from datetime import datetime
from datetime import timedelta, date

def ejecutarSentencia(querySQL, params):

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","Invoices" )
    cursor = db.cursor()

    rowsCount=cursor.execute(querySQL, params)

    db.commit()
    db.close()

    print("Registros actualizados {0}".format(rowsCount))

    return rowsCount

if __name__ == '__main__':

    print("**** Actualizar tablas espejo ***")

    params=[]	
    ejecutarSentencia("call spIPCLlenarTablasEspejo", params)	

