import requests
import json

def getOnuType(clientIp):
    # URL dasar API
    baseUrl = 'http://172.16.1.186:7557/devices'

    # Params WAN IP
    wanIp1 = "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress"
    wanIp2 = "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.2.WANPPPConnection.1.ExternalIPAddress"
    wanIp3 = "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.2.ExternalIPAddress"
    wanIp4 = "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.3.ExternalIPAddress"
    wanIp5 = "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.3.WANPPPConnection.1.ExternalIPAddress"

    wanIpList = [wanIp1, wanIp2, wanIp3, wanIp4, wanIp5]

    for wanIp in wanIpList:
        # Query untuk ExternalIPAddress (dibentuk sebagai string, bukan JSON)
        query = {wanIp: clientIp}

        # Proyeksi untuk _ProductClass
        projectionOnuType = '_deviceId._ProductClass'

        # Query deviceId dan wanIp
        result = {
            'deviceId': '',
            'onuType': ''
        }

        try:
            # Melakukan permintaan untuk mendapatkan ProductClass
            responseOnuType = requests.get(baseUrl, params={'query': json.dumps(query), 'projection': projectionOnuType}, timeout=10)

            # Cek status code
            if responseOnuType.status_code == 200:
                onuTypedata = responseOnuType.json()
                if onuTypedata == []:
                    continue                
                # Cek apakah ada data yang ditemukan
                elif onuTypedata:
                    # Mendapatkan ProductClass dan deviceId dari hasil pertama
                    deviceId = onuTypedata[0].get('_id', 'Unknown')  # Pastikan untuk mengambil deviceId yang benar
                    onuType = onuTypedata[0].get('_deviceId', {}).get('_ProductClass', 'Unknown')

                    result['deviceId'] = deviceId
                    result['onuType'] = onuType

                    return result
                else:
                    return 'No data found for given client IP'
            else:
                return f'Error {responseOnuType.status_code}: {responseOnuType.text}'
            
        except requests.exceptions.RequestException as e:
            # Tangkap error dari requests
            return f'Request failed: {str(e)}'