from datetime import datetime
import requests
import json
import pandas as pd
import time
import asyncio
import dbconnection as dbc
import os



async def DownloadStock(urlvtex, df_datos, marca):
        url_catalogo = urlvtex + "/api/catalog_system/pvt/sku/stockkeepingunitbyean/"
        url_stock = urlvtex + "/api/logistics/pvt/inventory/items/"
        
        df_vtex = pd.DataFrame(columns=['skuId', 'reference', 'total', 'reserved','available'])
        i = 1
        for item in range(len(df_datos)):
            try:
                if marca == 'BBW': reference = df_datos.loc[item, 'codbarras'] 
                else : reference = df_datos.loc[item, 'reference'] 
                
                response = requests.request("GET", url_catalogo + reference, headers=headers)
                # print(url_catalogo+reference)
                if len(response.text)>0:
                    jsoncatalogo = json.loads(response.text) 
            except Exception as e:
                print("Imposible descargar datos referencia: ", e)
            else:    
                try:
                     url_stock_get = url_stock + str(jsoncatalogo['Id'])  + "/warehouses/1_1"
                     response = requests.request("GET", url_stock_get, headers=headers)
                     jsonstock = json.loads(response.text)
                                
                except Exception as e:
                    print("Imposible descargar el Stock: ", e)
                else:
                    df_vtex.loc[len(df_vtex)] = [str(jsoncatalogo['Id']), reference, float(jsonstock[0]['totalQuantity']), float(jsonstock[0]['reservedQuantity']),float(jsonstock[0]['availableQuantity'])]
                    print(str(jsoncatalogo['Id']),reference, int(jsonstock[0]['totalQuantity']), int(jsonstock[0]['reservedQuantity']),int(jsonstock[0]['availableQuantity']),"línea : ", i)
                                
            i = i + 1
            if (i % 500) == 0:
                await asyncio.sleep(10)
                #time.sleep(0.75)
                print("Sleep", datetime.now())

        return(df_vtex)



# ##MAIN
try:
    pathuser = os.environ['USERPROFILE'] ##carpeta de usuario
    folderapp = os.getcwd() ##carpeta de ejecución de la app
    pathapp = folderapp + '\config.json'

    with open(pathapp, 'r') as file:
        data = json.load(file)
 
except IOError as e:
    ferror = open( pathuser + '/' + 'error.log', 'w')
    ferror.write(str(e))
    ferror.close()
else: 
    #ejecutar principal
    for i in data:
        marca = i
        for item in data[i]:
            print(datetime.now(), item['pais'])
            headers = {
                'content-type': "application/json",
                'accept': "application/json",
                'X-VTEX-API-AppKey' : item['appkey'],
                'X-VTEX-API-AppToken' : item['apptoken']
                }
            if item['status']=='1':
                
                conn = dbc.db_connect(item['ipserver'],item['database'],'icgadmin','masterkey')
                df_icg_stock =  dbc.db_stockarticulos(conn, item['codalmacen'], item['idtarifa'])
                # print(df_icg_stock.head)
                df_v = asyncio.run(DownloadStock(item['urlvtex'], df_icg_stock, marca))

                if not df_v.empty and not df_icg_stock.empty:
                    df_merge = pd.merge(df_v, df_icg_stock, on = ["reference"])

                    df_diff = df_merge.query("((stock-minimo) - available)>5")
                    if not df_diff.empty:
                        df_diff.to_excel('vtex_diff_' + item['pais'] + '.xlsx', index=False, header=True)
                        
                        #limpiar DF
                        if not df_icg_stock.empty: df_icg_stock = df_icg_stock.iloc[0:0]
                        if not df_v.empty:  df_v = df_v.iloc[0:0]


