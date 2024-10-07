import requests
import json

def getOnuType(clientIp):
    # URL dasar API
    baseUrl = 'http://172.16.1.186:7557/devices'

    # Params WAN IP
    wanIp1 = "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress" # F670L, F679, FD512XW-R460
    wanIp2 = "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.2.WANPPPConnection.1.ExternalIPAddress" # FD514GD-R460
    wanIp3 = "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.2.ExternalIPAddress" # F609, F660

    wanIpList = [wanIp1, wanIp2, wanIp3]

    for wanIp in wanIpList:
        # Query untuk ExternalIPAddress (dibentuk sebagai string, bukan JSON)
        query = {wanIp: clientIp}

        # Proyeksi untuk _ProductClass
        projectionOnuType = '_deviceId._ProductClass'

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
                    # Mendapatkan ProductClass dari hasil pertama
                    onuType = onuTypedata[0].get('_deviceId', {}).get('_ProductClass', 'Unknown')
                    return onuType
                else:
                    return 'No data found for given client IP'
            else:
                return f'Error {responseOnuType.status_code}: {responseOnuType.text}'
            
        except requests.exceptions.RequestException as e:
            # Tangkap error dari requests
            return f'Request failed: {str(e)}'