import pymysql
import json

def obtenerDatasetTotales(location, idTotal, databaseName, query):

    colNames = ["fecha", "usuario", "total1", "total2"]

    # MySQL Server credentials
    db = pymysql.connect( host="0.0.0.0", user="user", password="xxx", database=databaseName )
    cursor = db.cursor()
    
    rowsCount=cursor.execute(query)
    
    rows = []
    for data in cursor.fetchall():
        returnDataItem = {}
        returnDataItem["location"]=location
        returnDataItem["idTotal"]=idTotal
        colIndex = 0        
        for item in data:
            returnDataItem[colNames[colIndex]]=item
            colIndex = colIndex + 1
        rows.append(returnDataItem)

    db.close()

    return rows

if __name__ == '__main__':

    with open('totalesUpdateConf.json') as json_file:
        confTotales = json.load(json_file)
                      
    for currTotal in confTotales:
        print("..........................................")
        print(currTotal["database"])
        print(currTotal["idLocation"])
        print(currTotal["idTotal"])
        totalData = obtenerDatasetTotales(currTotal["idLocation"],currTotal["idTotal"],currTotal["database"], currTotal["query"])
        #for totRow in totalData:
        #    print("{0} {1} {2} {3} {4} {5}".format(currTotal["idLocation"], currTotal["idTotal"], totRow["Fecha"], totRow["usuario"], totRow["total1"],  totRow["total2"]))
        #print(json.dumps(totalData))
        with open("Totales_" + currTotal["idLocation"] + ".json", "w") as f:
            f.write(json.dumps(totalData))
