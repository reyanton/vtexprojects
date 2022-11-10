import pandas as pd
import pyodbc 


def db_connect(servername, dbname, username, passuser):
    try:
        conn = pyodbc.connect('Driver={SQL Server}; Server=' + servername + ';Database=' + dbname + ';UID=' + username + ';PWD=' + passuser + ';')

        return(conn)    
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

    

def db_stockarticulos(conn, codalmacen,idtarifa):
    try:
        df = pd.read_sql_query("SELECT REFPROVEEDOR as reference, codbarras,  stock, minimo, fechastock, PNETO, PBRUTO  FROM vwstockTarifa where codalmacen = '" + codalmacen + "' and idtarifav = " + str(idtarifa), conn)
        
        return(df)
    except Exception as e:
        print("Ocurrió un error al consultar Stock: ", e)
        
def db_datosclientes(conn, anio):    
    try:
        query = "select anio, mes, nuevo, recurrente from vwclientesecommerce where anio = " + str(anio) + "  order by 1, 2"
        df = pd.read_sql_query(query, conn)
        return(df)
    except Exception as e:
        print("Ocurrió un error al consultar clientes: ", e)

def db_rfmdata(conn):    
    try:
        query = "exec spRMF"
        df = pd.read_sql_query(query, conn)
        return(df)
    except Exception as e:
        print("Ocurrió un cargar datos del RFM: ", e)
#main

