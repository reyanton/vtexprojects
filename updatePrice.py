import requests
import json

url = "https://victoriassecretbeautyar.myvtex.com/api/pricing/prices/2147"
url_2 = "/warehouses/"

payload = {
    "markup": 0,
    "listPrice": 550,
    "basePrice": 550,
    
}

headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'X-VTEX-API-AppKey' : "vtexappkey-victoriassecretbeautyar-JNQSFS",
    'X-VTEX-API-AppToken' : "YRANKKORVOXQMPGRGCMHMAACTYHHERYQPXKAMDQEXBMSVFNIHSNSIVNXRYTLCGMEQHBOFFEDLIJLOIGOKZALDFHTKMJOKFBQOIBODYDBOKHZLCJISEADGAALZHESVPTG"
    }

response = requests.request("PUT", url, headers=headers, json=payload)

print(response.text)