import requests
import json
import pymysql
#import datetime
from datetime import datetime
from datetime import timedelta, date

def ejecutarSentencia(querySQL, params):

    # MySQL Server credentials
    db = pymysql.connect("45.55.248.209","root","F3rn4nd0M","Invoices" )
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

