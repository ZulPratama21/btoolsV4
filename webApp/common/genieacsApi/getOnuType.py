import requests
import json

def getOnuType(clientIp):
    # URL dasar API
    baseUrl = 'http://172.16.1.186:7557/devices'

    # Query untuk ExternalIPAddress
    query = json.dumps({
        "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress": clientIp
    })

    # Proyeksi untuk SSID dan KeyPassphrase
    projectionOnuType = '_deviceId._ProductClass'

    try:
        # Melakukan permintaan untuk SSID
        responseOnuType = requests.get(baseUrl, params={'query': query, 'projection':projectionOnuType})
        if responseOnuType.status_code == 200:
            onuTypedata = responseOnuType.json()
            onuType = onuTypedata[0]['_deviceId']['_ProductClass']

            return onuType

        else:
            return responseOnuType.status_code + ', ' +  responseOnuType.text
        
    except Exception as e:
        return str(e)