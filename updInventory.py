import requests
import json

url = "https://victoriassecretbeautype.myvtex.com/api/logistics/pvt/inventory/skus/"
url_2 = "/warehouses/"

sku = "195"
wh = "1_1"

url_req = url + sku + url_2 + wh

datastock = {
    'unlimitedQuantity': False,
    'dateUtcOnBalanceSystem': None,
    'quantity': 54
}

headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'X-VTEX-API-AppKey' : "vtexappkey-victoriassecretbeautyar-JNQSFS",
    'X-VTEX-API-AppToken' : "YRANKKORVOXQMPGRGCMHMAACTYHHERYQPXKAMDQEXBMSVFNIHSNSIVNXRYTLCGMEQHBOFFEDLIJLOIGOKZALDFHTKMJOKFBQOIBODYDBOKHZLCJISEADGAALZHESVPTG"
    }

print(datastock)
response = requests.request("PUT", url_req, headers=headers, json=datastock)

print(response.text)