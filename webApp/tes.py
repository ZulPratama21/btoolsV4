# Supported device: F670L, F679L
import requests
import json

def getData(clientIp):
    # URL dasar API
    baseUrl = 'http://172.16.1.186:7557/devices'
    timeout = 3  # Batas waktu 3 detik

    # Query untuk ExternalIPAddress
    query = json.dumps({
        "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress": clientIp
    })
    
    result = {
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
    projectionSsid5 = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.SSID._value"
    projectionSsid2 = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID._value"
    projectionKeypassphrase5 = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.KeyPassphrase._value"
    projectionKeypassphrase2 = "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.KeyPassphrase._value"
    projectionHost = 'InternetGatewayDevice.LANDevice.1.Hosts.Host'
    
    # Melakukan permintaan untuk SSID 5.8 Ghz
    try:
        responseSsid5 = requests.get(baseUrl, params={'query': query, 'projection': projectionSsid5}, timeout=timeout)
        if responseSsid5.status_code == 200:
            ssidData5 = responseSsid5.json()
            ssid5 = ssidData5[0]['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['5']['SSID']['_value']

            result['ssid']['5.8'] = ssid5 

        else:
            result["ssid"]['5.8'] = responseSsid5.status_code + ', ' +  responseSsid5.text

    except IndexError:
        result['ssid']['5.8'] = 'not found'

    except requests.exceptions.Timeout:
        result['ssid']['5.8'] = 'request timed out'

    except Exception as e:
        result['ssid']['5.8'] = 'error: ' + str(e)

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

    # Melakukan permintaan untuk KeyPassphrase 5.8 Ghz
    try:
        responseKeypassphrase5 = requests.get(baseUrl, params={'query': query, 'projection': projectionKeypassphrase5}, timeout=timeout)
        if responseKeypassphrase5.status_code == 200:
            keypassphraseData2 = responseKeypassphrase5.json()
            keypassphrase2 = keypassphraseData2[0]['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['5']['KeyPassphrase']['_value']
            result['passWifi']['5.8'] = keypassphrase2
            
        else:
            result['passWifi']['5.8'] = responseKeypassphrase5.status_code + ', ' + responseKeypassphrase5.text

    except IndexError:
        result['passWifi']['5.8'] = 'not found'

    except requests.exceptions.Timeout:
        result['passWifi']['5.8'] = 'request timed out'

    except Exception as e:
        result['passWifi']['5.8'] = 'error: ' + str(e)

    # Melakukan permintaan untuk KeyPassphrase 2.4 Ghz
    try:
        responseKeypassphrase2 = requests.get(baseUrl, params={'query': query, 'projection': projectionKeypassphrase2}, timeout=timeout)
        if responseKeypassphrase2.status_code == 200:
            keypassphraseData5 = responseKeypassphrase2.json()
            keypassphrase5 = keypassphraseData5[0]['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['1']['KeyPassphrase']['_value']
            result['passWifi']['2.4'] = keypassphrase5
            
        else:
            result['passWifi']['2.4'] = responseKeypassphrase2.status_code + ', ' + responseKeypassphrase5.text

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

        else:
            result['connectedDevice'] = responseHost.status_code + ', ' + responseHost.text

    except IndexError:
        result['connectedDevice'] = 'not found'

    except requests.exceptions.Timeout:
        result['connectedDevice'] = 'request timed out'

    except Exception as e:
        result['connectedDevice'] = str(e)

    return result

def getDeviceIdByIp(clientIP):
    # URL untuk mendapatkan devices berdasarkan IP address
    baseUrl = 'http://172.16.1.186:7557/devices'
    timeout = 3  # Batas waktu 3 detik
    
    # Query berdasarkan IP address
    query = json.dumps({
        "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress": clientIP
    })
    
    try:
        response = requests.get(baseUrl, params={'query': query}, timeout=timeout)
        if response.status_code == 200:
            devices = response.json()
            if devices:
                deviceId = devices[0]["_id"]
                return deviceId
            else:
                return None
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None

output = getDeviceIdByIp('10.201.47.4')
print(json.dumps(output, indent=4))