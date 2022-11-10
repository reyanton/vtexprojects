import requests
import json

headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'X-VTEX-API-AppKey' : "vtexappkey-bathbody-DZKCBN",
        'X-VTEX-API-AppToken' : "WMADGGFOYDQEDDVGUYXZMQPGQATUPXPJHMDAVXQPGEQBIGGIKJBAVFTGWTNFMKYBOHWRAUKXIISIZNYJUKKGVONBSXDBJKCWFONAJOIPYESNNKGJVELCASFZUVYCQJNY"
        }

def get_stock_details(item, warehouse):
    global headers

    url = "https://bathbody.myvtex.com/api/logistics/pvt/inventory/items/"
    url_wh = "/warehouses/"
    
    url_stock = url + item + url_wh + warehouse

    response = requests.request("GET", url_stock, headers=headers)
    json_list = json.loads(response.text)
    
    return(json_list)

def get_EAN(item):
    global headers

    url = "https://bathbody.myvtex.com/api/catalog/pvt/product/"

    url_EAN = url + item
    response = requests.request("GET", url_EAN, headers=headers)
    json_list = json.loads(response.text)
    
    return(json_list)

def get_product_details(item):
    global headers

    url = "https://bathbody.myvtex.com/api/catalog/pvt/stockkeepingunit/"

    url_prod = url + item
    response = requests.request("GET", url_prod, headers=headers)
    json_list = json.loads(response.text)
    
    return(json_list)