import requests
import json

headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'X-VTEX-API-AppKey' : "vtexappkey-victoriassecretbeautype-GUBDMD",
    'X-VTEX-API-AppToken' : "UVLIZQPJFGJXXCVNYBXSEZKWJUAIIGOWJNQDVQUEHFXLXOHKUCTLUMVUKPZFQHBZSMOKMRRHHSKYCYZUMPNFMDCWSVTGRPNZEYTKAXYCLMEBBWSLPFSBTVMPJRRQYKQR"
    }

url = "https://victoriassecretbeautype.myvtex.com/api/logistics/pvt/inventory/skus/"
url_2 = "/warehouses/"

def GetSku_Id(sEAN):
    url_sku = "https://victoriassecretbeautype.myvtex.com/api/catalog_system/pvt/sku/stockkeepingunitbyean/"
    url_sku = url_sku + sEAN
    print(url_sku)
    response_sku = requests.request("GET", url_sku, headers=headers)
    jsonlist = json.loads(response_sku.text)
    return(jsonlist['Id'])

Id_Sku = GetSku_Id("23836689")
print(Id_Sku)

# sku = "195"
# wh = "1_1"

# url_req = url + sku + url_2 + wh

# datastock = {}
# datastock["unlimitedQuantity"] = False
# datastock["dateUtcOnBalanceSystem"] = None
# datastock["quantity"] = 54

# # datastock = {
# #     'unlimitedQuantity': False,
# #     'dateUtcOnBalanceSystem': None,
# #     'quantity': 54
# # }



# print(datastock)
# # response = requests.request("PUT", url_req, headers=headers, json=datastock)

# # print(response.text)