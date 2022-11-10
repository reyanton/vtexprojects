import requests
import json

url = "https://victoriassecretbeautycr.myvtex.com/api/oms/pvt/orders/1252120131193-01/changestate/invoice"#?_from=100&_to=119" #fq=B:2000000"
url2 = "https://victoriassecretbeautypa.myvtex.com/api/catalog_system/pub/products/offers/1216/sku/2147"
urllog = "https://victoriassecretbeautype.myvtex.com/api/pvt/transactions/94B32819CFF64DF9965A678C364B62F8"

headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'X-VTEX-API-AppKey' : "vtexappkey-victoriassecretbeautype-GUBDMD",
    'X-VTEX-API-AppToken' : "UVLIZQPJFGJXXCVNYBXSEZKWJUAIIGOWJNQDVQUEHFXLXOHKUCTLUMVUKPZFQHBZSMOKMRRHHSKYCYZUMPNFMDCWSVTGRPNZEYTKAXYCLMEBBWSLPFSBTVMPJRRQYKQR"
    }


response = requests.request("GET", urllog, headers=headers)
# jsonCat = json.loads(response.text)

print(response)


# import requests

# url = "https://.api.com.br/api/catalog_system/pub/products/search?_from=1&_to=50&ft=television&fq=C%3A%2F1000041%2F1000049%2F&O=OrderByNameASC"

# headers = {"Accept": "application/json"}

# response = requests.get(url, headers=headers)

# print(response.text)