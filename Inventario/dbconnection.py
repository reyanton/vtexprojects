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
        # print(df)
        return(df)
    except Exception as e:
        print("Ocurrió un error al consultar Stock: ", e)
        
    


#main

