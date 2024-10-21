from routeros_api import RouterOsApiPool
import json

connection = RouterOsApiPool(
    host='103.73.72.9',
    username='jul',
    password='Juliandi123!@#',
    port=8728,
    plaintext_login=True
)
api = connection.get_api()

getAddress = api.get_resource('/ip/address')
allAddress = getAddress.get(address='103.73.72.9/32')

print(json.dumps(allAddress, indent=4))