import pymysql
import json

def crearRegistroDeEnvio(nombreEnvio):

    # MySQL Server credentials
    db = pymysql.connect( host="0.0.0.0", user="user", password="xxx", database="Invoices" )
    cursor = db.cursor()
    
    lQueryInsert = "INSERT INTO catEnvios(dtFechaProcesada,cTipoEnvio) VALUES(NOW(),'{0}');".format(nombreEnvio)
    
    rowsCount=cursor.execute(lQueryInsert)
    retValue = db.insert_id()
    
    db.commit()      
    db.close()

    return retValue

def obtenerDatasetTotales(query):

    colNames = ["usuario", "campo1", "campo2", "fecha", "maxDate"]

    # MySQL Server credentials
    db = pymysql.connect( host="0.0.0.0", user="user", password="xxx", database="Invoices" )
    cursor = db.cursor()
    
    rowsCount=cursor.execute(query)
    
    rows = []
    for data in cursor.fetchall():
        returnDataItem = {}
        colIndex = 0        
        for item in data:
            returnDataItem[colNames[colIndex]]=item
            colIndex = colIndex + 1
        rows.append(returnDataItem)

    db.close()

    return rows
    
def convertirAIdUsuario(usuario):

    # MySQL Server credentials
    db = pymysql.connect( host="0.0.0.0", user="user", password="xxx", database="Invoices" )
    cursor = db.cursor()
    
    rowsCount=cursor.execute("SELECT iidusuario from catUsuarios where clogin = '{0}'".format(usuario))
    
    idUsuario = -1
    for data in cursor.fetchall():
        idUsuario = data[0]

    db.close()
    return idUsuario
    
def generarConsultaParaUpdateLocal(lQueryTemplate, lArrayParams, lDataSource, idEnvio, obtenerIdUsuario):

    localQry = lQueryTemplate.format(idEnvio)   

    for currParam in lArrayParams:
        parameterString = "**{0}**".format(currParam)
        paramToUse = currParam
        if currParam == "usuario" and obtenerIdUsuario == "True":
            localQry = localQry.replace(parameterString, "{0}".format(convertirAIdUsuario(lDataSource[currParam])))
        else:
            localQry = localQry.replace(parameterString, "{0}".format(lDataSource[paramToUse]))
        
    return localQry
    
def marcarComoEnviados(lQueryUpdate):

    # MySQL Server credentials
    db = pymysql.connect( host="0.0.0.0", user="user", password="xxx", database="Invoices" )
    cursor = db.cursor()
     
    #print(lQueryUpdate)
    rowsCount=cursor.execute(lQueryUpdate)
    
    db.commit()      
    db.close()

if __name__ == '__main__':

    with open('totalesConf.json') as json_file:
        confTotales = json.load(json_file)
                      
    for currTotal in confTotales:
        print("..........................................")
        idEnvio = crearRegistroDeEnvio(currTotal["nombre"])    
        print("Actualizando {0}, envio {1}".format(currTotal["nombre"], idEnvio))
        totalNotas = obtenerDatasetTotales(currTotal["consulta"])
        for currTotData in totalNotas:
            print("{0}, {1}, {2}, {3}, {4}".format(currTotData["usuario"], 
                                                   currTotData["campo1"], 
                                                   currTotData["campo2"], 
                                                   currTotData["fecha"], 
                                                   currTotData["maxDate"] ))
            consultaUpdate=generarConsultaParaUpdateLocal(currTotal["consultaUpdate"], 
                                                          currTotal["pramaetrosUpdate"], 
                                                          currTotData, 
                                                          idEnvio, 
                                                          currTotal["obtenerIdUsuario"])
            print(consultaUpdate)
            #marcarComoEnviados(consultaUpdate)
    
