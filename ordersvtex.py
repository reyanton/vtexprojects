import requests
import json
import pandas as pd
from datetime import datetime, timedelta, timezone
import timezone as tz

dia = datetime.now()

file_name_excel = "C:\Proyectos\Vtex APIs\listado_ordenes_" + dia.strftime("%Y%m%d-%H%M%S") + ".xlsx"

dia = dia - timedelta(days=1)

strDia = dia.strftime("%Y/%m/%d") 

strFechas = tz.asignar_time(strDia,strDia)

strRango = "creationDate:[" + strFechas + "]"

urllistord = "https://bathbody.myvtex.com/api/oms/pvt/orders?per_page=100&page="
urlord = "https://bathbody.myvtex.com/api/oms/pvt/orders"

#querystring = {"f_creationDate":"creationDate:[2020-09-01T00:00:00.000Z TO 2020-09-01T23:59:59.999Z]"}
querystring =  {"f_creationDate":strRango}
headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'X-VTEX-API-AppKey' : "vtexappkey-bathbody-DZKCBN",
    'X-VTEX-API-AppToken' : "WMADGGFOYDQEDDVGUYXZMQPGQATUPXPJHMDAVXQPGEQBIGGIKJBAVFTGWTNFMKYBOHWRAUKXIISIZNYJUKKGVONBSXDBJKCWFONAJOIPYESNNKGJVELCASFZUVYCQJNY"
    }

list_orders = []
orders_det = []
totorders = 0
countorders = 0
numpag = 0
pag = 0

while True:
    urllist = urllistord + str(pag+1)
    
    if numpag != 0 and numpag == pag: break
    print(querystring)    
    responselist = requests.request("GET", urllist, headers=headers, params=querystring)
    
    jsonlist = json.loads(responselist.text)
    if numpag == 0: 
        numpag = int(jsonlist['paging']['pages'])
    
    for item in jsonlist['list']:
        #if item['status'] == 'canceled':
        list_orders.append(item['orderId'])

    pag = pag + 1

for lst in list_orders:
    urlorder = urlord + "/" + lst
    
    responseorder = requests.request("GET", urlorder, headers=headers, params=querystring)
    jsonorder = json.loads(responseorder.text)

    # print(jsonorder)
    localdate = datetime.strptime(jsonorder['creationDate'][:10] + ' ' + jsonorder['creationDate'][11:19], '%Y-%m-%d %H:%M:%S') - timedelta(hours=5) 
    localdate = datetime.strftime(localdate, '%Y-%m-%d %H:%M:%S')
    orders_det.append((lst, 
        #jsonorder['creationDate'],
        localdate,
        jsonorder['statusDescription'],
        (float(jsonorder['value'])/100),
        jsonorder['clientProfileData']['firstName'] + ' ' + jsonorder['clientProfileData']['lastName'],
        jsonorder['paymentData']['transactions'][0]['payments'][0]['paymentSystemName'],
        str(jsonorder['paymentData']['transactions'][0]['payments'][0]['firstDigits']) + '****' + str(jsonorder['paymentData']['transactions'][0]['payments'][0]['lastDigits']),
        jsonorder['paymentData']['transactions'][0]['payments'][0]['tid']
        ))

    totorders = totorders + (float(jsonorder['value'])/100)
    countorders = countorders + 1
        
df = pd.DataFrame.from_records(orders_det, columns =['OrderId', 'Fecha', 'Estatus', 'Monto', 'Cliente', 'Pago','Tarjeta','Transacción']) 
#df.to_csv(file_name, encoding='utf-8', index=False)
df.to_excel (file_name_excel, index = False, header=True)

print(df)
print("total : ", totorders)
print("#ordenes : ", countorders)
