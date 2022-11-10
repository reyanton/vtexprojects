import pyodbc
import pandas as pd
import dbconnection as dbc 
import json


def get_customers_db(servername:str,dbname:str):       
    try:
        
        conn = dbc.db_connect(servername, dbname,'icgadmin','masterkey')
        dfcustomers = dbc.db_datosclientes(conn, 2022)
        
        js = dfcustomers.to_json(orient = 'records')
        parsed = json.loads(js)       

    except Exception as e:
        print("Error cargando datos clientes : ", e)
    else:
        return (json.dumps(parsed, indent=4)), 201

def get_sales_db(servername:str,dbname:str):
    try:
        
        conn = dbc.db_connect(servername, dbname,'icgadmin','masterkey')
        dfsales = dbc.db_rfmdata(conn)
        
        js = dfsales.to_json(orient = 'records')
        parsed = json.loads(js)       

    except Exception as e:
        print("Error cargando datos de ventas : ", e)
    else:
        return (json.dumps(parsed, indent=4)), 201