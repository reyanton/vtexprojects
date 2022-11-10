import requests


headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'X-VTEX-API-AppKey' : "vtexappkey-bathbodyco-GRVMXX",
    'X-VTEX-API-AppToken' : "YMFDDIUYZHDHNSBJZYOQNJSCVUZEJKSCDMVYRQEHCVWANQJDMNNCCPVPUCIIJQOPPAEBXDRITGORMROFLVRVWPANQGDOIVYLGHLMLIGJWFIVAECCODXNZSSZZRKRZCZY"
    }

order_id = '00-1268440664182-01'

# url2 =  "https://victoriassecretbeautyco.myvtex.com/api/logistics/pvt/inventory/reservations/1/2232"


url = "https://bathbodyco.myvtex.com/api/logistics/pvt/inventory/reservations/" + order_id  +"/cancel"

response = requests.post(url, headers=headers)

print(response.text)