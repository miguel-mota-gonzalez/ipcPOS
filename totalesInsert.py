import pymysql
import json
import os

#{"total1": 23, "total2": 1.0, "fecha": "2022-4-1 17:00:00", "usuario": "geny", "idTotal": "5", "location": "107"}
#mysql> describe detTotalPorDia;
#+-------------------+--------------+------+-----+---------+----------------+
#| Field             | Type         | Null | Key | Default | Extra          |
#+-------------------+--------------+------+-----+---------+----------------+
#| idDetTotalId      | int(11)      | NO   | PRI | NULL    | auto_increment |
#| idLocacion        | bigint(20)   | NO   | PRI | NULL    |                |
#| idTotal           | bigint(20)   | NO   | PRI | NULL    |                |
#| dtFecha           | date         | NO   | PRI | NULL    |                |
#| cCajero           | varchar(256) | NO   | PRI | NULL    |                |
#| dTotal            | double       | NO   |     | NULL    |                |
#| dTotal2           | double       | NO   | MUL | NULL    |                |
#| dtFechaAlta       | datetime     | NO   |     | NULL    |                |
#| dtFechaAct        | datetime     | NO   |     | NULL    |                |
#| iProcesadoAlmacen | int(11)      | YES  |     | 0       |                |
#+-------------------+--------------+------+-----+---------+----------------+
#10 rows in set (0.02 sec)

def insertarTotal(pQuery):

    content = request.json

    # MySQL Server credentials
    db = pymysql.connect("0.0.0.0","user","xxx","eboxglobal" )
    cursor = db.cursor()
    
    rowsCount=cursor.execute(pQuery)
    
    db.commit()      
    db.close()

    return jsonify(isError=False, updated=rowsCount, statusCode=200, qry=lQuery)

if __name__ == '__main__':

    arr = os.listdir('./totalesInput')
    for archivo in arr:
        with open("./totalesInput/" + archivo) as json_file:
            confTotales = json.load(json_file)
            for currTotal in confTotales:
                print("insert into detTotalPorDia(idLocacion,idTotal,dtFecha,cCajero,dTotal,dTotal2,dtFechaAlta,dtFechaAct,iProcesadoAlmacen) values({0},{1},'{2}','{3}',{4},{5},NOW(),NOW(),0);".format(
                currTotal["location"],currTotal["idTotal"],currTotal["fecha"],currTotal["usuario"],currTotal["total1"],currTotal["total2"]))
		#print(insertarTotal("insert into detTotalPorDia(idLocacion,idTotal,dtFecha,cCajero,dTotal,dTotal2,dtFechaAlta,dtFechaAct,iProcesadoAlmacen) values({0},{1},'{2}','{3}',{4},{5},NOW(),NOW(),0);".format(currTotal["location"],currTotal["idTotal"],currTotal["fecha"],currTotal["usuario"],currTotal["total1"],currTotal["total2"])))
