import requests
import json
import pandas as pd
from datetime import datetime, timedelta, timezone
import timezone as tz


end_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
ini_prev_month = datetime.today().replace(day=1) - timedelta(days=end_prev_month.day)

file_name_excel = "C:\Proyectos\Vtex APIs\listado_ordenes_PER_" + ini_prev_month.strftime("%Y%m%d") + "_" + end_prev_month.strftime("%Y%m%d") + ".xlsx"

#dia = datetime.now()

#dia = dia - timedelta(days=1)

strIniMonth = ini_prev_month.strftime("%Y/%m/%d")
strEndMonth = end_prev_month.strftime("%Y/%m/%d")
#strDia = dia.strftime("%Y/%m/%d") 

strFechas = tz.format_time(strIniMonth,strEndMonth)

strRango = "creationDate:[" + strFechas + "]"

urllistord = "https://bathbodype.myvtex.com/api/oms/pvt/orders?per_page=100&page="
urlord = "https://bathbodype.myvtex.com/api/oms/pvt/orders"

#querystring = {"f_creationDate":"creationDate:[2020-09-01T00:00:00.000Z TO 2020-09-01T23:59:59.999Z]"}
querystring =  {"f_creationDate":strRango}
headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'X-VTEX-API-AppKey' : "vtexappkey-bathbodype-PHKUTJ",
    'X-VTEX-API-AppToken' : "OZPPKFEOMNLXPRUXZZXMFOOUORKYNQXDJBDMDRHDIDFFSRTBCVTNLWRZLVBTUFBVQHNOOITIRUEBJIBXYJWSXKRMKDBHQNICCJOLDFMTBLVRSPQCUEVLJJYFQADKHMSD"
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
    print(jsonorder)
    localdate = datetime.strptime(jsonorder['creationDate'][:10] + ' ' + jsonorder['creationDate'][11:19], '%Y-%m-%d %H:%M:%S') - timedelta(hours=5) 
    localdate = datetime.strftime(localdate, '%Y-%m-%d %H:%M:%S')
    orders_det.append((lst, 
        jsonorder['creationDate'],
        #localdate,
        jsonorder['statusDescription'],
        (float(jsonorder['value'])/100),
        jsonorder['clientProfileData']['firstName'] + ' ' + jsonorder['clientProfileData']['lastName'],
        jsonorder['paymentData']['transactions'][0]['payments'][0]['paymentSystemName'],
        #jsonorder['paymentData']['transactions'][0]['payments'][0]['firstDigits'] + '****' + jsonorder['paymentData']['transactions'][0]['payments'][0]['lastDigits'],
        jsonorder['paymentData']['transactions'][0]['payments'][0]['tid']
        ))

    totorders = totorders + (float(jsonorder['value'])/100)
    countorders = countorders + 1
    
df = pd.DataFrame.from_records(orders_det, columns =['OrderId', 'Fecha', 'Estatus', 'Monto', 'Cliente', 'Pago','Transacción']) 
#df.to_csv(file_name, encoding='utf-8', index=False)
df.to_excel (file_name_excel, index = False, header=True)

print(df)
print("total : ", totorders)
print("#ordenes : ", countorders)
