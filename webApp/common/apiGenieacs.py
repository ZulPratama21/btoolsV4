import requests
import json

def getData(clientIp):
    # URL dasar API
    baseUrl = 'http://172.16.1.186:7557/devices'

    # Query untuk ExternalIPAddress
    query = json.dumps({
        "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress": clientIp
    })

    result = {}

    # Proyeksi data yang akan diambil
    projectionSsid = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID._value"
    projectionKeypassphrase = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.X_CMS_KeyPassphrase._value"
    projectionRxPower = "InternetGatewayDevice.DeviceInfo.XponInterface.RXPower._value"

    try:
        # Melakukan permintaan untuk SSID
        responseSsid = requests.get(baseUrl, params={'query': query, 'projection': projectionSsid})
        if responseSsid.status_code == 200:
            ssidData = responseSsid.json()
            ssid = ssidData[0]['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['1']['SSID']['_value']

            result['ssid'] = ssid 

        else:
            result["ssid"] = responseSsid.status_code + ', ' +  responseSsid.text

        # Melakukan permintaan untuk KeyPassphrase
        responseKeypassphrase = requests.get(baseUrl, params={'query': query, 'projection': projectionKeypassphrase})
        if responseKeypassphrase.status_code == 200:
            keypassphraseData = responseKeypassphrase.json()
            keypassphrase = keypassphraseData[0]['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['1']['X_CMS_KeyPassphrase']['_value']
            result['keypassphrase'] = keypassphrase
            
        else:
            result["keyPassphrase"] = responseKeypassphrase.status_code + ', ' + responseKeypassphrase.text

        '''
        # Melakukan permintaan untuk KeyPassphrase
        responseRxPower = requests.get(baseUrl, params={'query': query, 'projection': projectionRxPower})
        if responseRxPower.status_code == 200:
            rxPowerData = responseRxPower.json()
            rxPower = rxPowerData[0]['InternetGatewayDevice']['DeviceInfo']['XponInterface']['RXPower']['_value']
            result['rxPower'] = rxPower
            
        else:
            result["keyPassphrase"] = responseRxPower.status_code + ', ' + responseRxPower.text
        '''
            
    except Exception as e:
        result['ssid'] = 'error'
        result['keyPassphrase'] = str(e)
        # result['rxPower'] = str(e)

    return result

output = getData('10.201.35.153')

print(json.dumps(output, indent=4))