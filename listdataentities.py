import requests
import json


headers = {
    'content-type': "application/json",
    'accept': "application/json",
    "REST-Range": "resources=0-2000",
    'X-VTEX-API-AppKey' : "vtexappkey-victoriassecretbeautyco-JISGDP",
    'X-VTEX-API-AppToken' : "IFMKNEPFRNJBUYRPZZZSJDXYXNZKVIZSPIUXCCPIQJCLGVRRHFQGELYFHNNZFFJINQMLETMXKRBAAMRBVHDQRTNDKPQOOPDKZTXPJFMNSTVNJXEVVLDXCTRTCJBPDYIU"
    }


url = "https://victoriassecretbeautyco.myvtex.com/api/dataentities"

url_customers = "https://victoriassecretbeautyco.myvtex.com/api/dataentities/CL/search?_fields=email,firstName,lastName,createdIn,document&_where=createdIn between 2022-01-01 AND 2022-03-31"

url_customers_schema = "https://victoriassecretbeautyco.myvtex.com/api/dataentities/CL"

response = requests.get(url_customers_schema, headers=headers)
jsondata  = json.loads(response.text)
print(jsondata)

# i = 1
# for item in jsondata:
#     print(item['email'])
#     i = i + 1

# print("listado de:", i)