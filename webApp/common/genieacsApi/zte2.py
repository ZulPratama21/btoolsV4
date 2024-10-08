# Supported device: F609

import requests
import json

def getData(deviceId):
    # URL dasar API
    baseUrl = 'http://172.16.1.186:7557/devices'
    timeout = 3  # Batas waktu 3 detik

    # Query untuk ExternalIPAddress
    query = json.dumps({
        '_id': deviceId
    })
    
    result = {
        'deviceId':deviceId,
        'ssid': {
            '5.8': '',
            '2.4': '',
        },
        'passWifi': {
            '5.8': '',
            '2.4': '',
        },
        'connectedDevice': '',
    }

    # Proyeksi data yang akan diambil
    projectionSsid2 = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID._value"
    projectionKeypassphrase2 = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.PreSharedKey.1.KeyPassphrase._value"
    projectionHost = 'InternetGatewayDevice.LANDevice.1.Hosts.Host'

    # Melakukan permintaan untuk SSID 2.4 Ghz
    try:
        responseSsid2 = requests.get(baseUrl, params={'query': query, 'projection': projectionSsid2}, timeout=timeout)
        if responseSsid2.status_code == 200:
            ssidData2 = responseSsid2.json()
            ssid2 = ssidData2[0]['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['1']['SSID']['_value']

            result['ssid']['2.4'] = ssid2 

        else:
            result["ssid"]['2.4'] = responseSsid2.status_code + ', ' +  responseSsid2.text

    except IndexError:
        result['ssid']['2.4'] = 'not found'

    except requests.exceptions.Timeout:
        result['ssid']['2.4'] = 'request timed out'

    except Exception as e:
        result['ssid']['2.4'] = str(e)
        
    # Melakukan permintaan untuk KeyPassphrase 2.4 Ghz
    try:
        responseKeypassphrase2 = requests.get(baseUrl, params={'query': query, 'projection': projectionKeypassphrase2}, timeout=timeout)
        if responseKeypassphrase2.status_code == 200:
            keypassphraseData2 = responseKeypassphrase2.json()
            keypassphrase2 = keypassphraseData2[0]['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['1']['PreSharedKey']['1']['KeyPassphrase']['_value']
            result['passWifi']['2.4'] = keypassphrase2
            
        else:
            result['passWifi']['2.4'] = responseKeypassphrase2.status_code + ', ' + responseKeypassphrase2.text

    except IndexError:
        result['passWifi']['2.4'] = 'not found'

    except requests.exceptions.Timeout:
        result['passWifi']['2.4'] = 'request timed out'

    except Exception as e:
        result['passWifi']['2.4'] = 'error: ' + str(e)
    
    # Melakukan permintaan untuk jumlah host terhubung
    try:
        responseHost = requests.get(baseUrl, params={'query': query, 'projection':projectionHost}, timeout=timeout)
        if responseHost.status_code == 200:
            hostData = responseHost.json()
            host = hostData[0]['InternetGatewayDevice']['LANDevice']['1']['Hosts']['Host']

            connectedDevice = []

            for x in host:
                if not x.isdigit():
                    break
                hostName = host[x]['HostName']['_value']
                ipAddress = host[x]['IPAddress']['_value']
                macAddress = host[x]['MACAddress']['_value']

                connectedDevice.append({
                    'hostName': hostName,
                    'ipAddress': ipAddress,
                    'macAddress': macAddress,
                })
            
            result['connectedDevice'] = connectedDevice
            result['totalConnDevice'] = len(connectedDevice)

        else:
            result['connectedDevice'] = responseHost.status_code + ', ' + responseHost.text
            result['totalConnDevice'] = responseHost.status_code + ', ' + responseHost.text

    except IndexError:
        result['connectedDevice'] = 'not found'

    except requests.exceptions.Timeout:
        result['connectedDevice'] = 'request timed out'

    except Exception as e:
        result['connectedDevice'] = str(e)

    return result

def setWifi(deviceId, band, ssid, passWifi):

    paramSsid = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID"
    paramPassWifi = 'InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.PreSharedKey.1.KeyPassphrase'

    # URL dasar API dengan deviceId
    baseUrl = f'http://172.16.1.186:7557/devices/{deviceId}/tasks?timeout=3000&connection_request'
    
    # Data yang akan dikirimkan
    data = {
        "name": "setParameterValues",
        "parameterValues": [
            [paramSsid, ssid] , [paramPassWifi, passWifi]
        ]
    }

    result = {
        'statusCode': '',
        'responseBody': ''
    }

    # Melakukan permintaan POST ke API
    try:
        response = requests.post(baseUrl, json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result['statusCode'] = response.status_code
            result['responseBody'] = f'Berhasil konfigurasi wifi<br>SSID: <strong>{ssid}</strong><br>Password: <strong>{passWifi}</strong><br>'

        else:
            result['statusCode'] = response.status_code
            result['responseBody'] = response.text

    except Exception as e:
        result['statusCode'] = 'error'
        result['responseBody'] = str(e)

    return result