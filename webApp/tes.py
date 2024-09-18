from routeros_api import RouterOsApiPool
import json

def get_traffic_data():
    inputUser = 'ca0019001'
    idlocation = inputUser.upper()

    connection = RouterOsApiPool(
        '103.73.72.162',
        username='jul',
        password='Juliandi123!@#',
        port=8728,
        plaintext_login=True
    )
    api = connection.get_api()

    secrets = api.get_resource('/ppp/secret')
    allSecret = secrets.get()

    for secret in allSecret:
        comment = secret['comment']
        if idlocation in comment:
            # Mengambil Kode NE untuk kebutuhan troubleshoot
            commentId = comment.split()[0]
            neCode = commentId.split('-')[1]

            # Mengambil ip address client untuk melakukan ping
            remoteAddress = secret['remote-address']
            break

    pingResult = api.get_resource('/').call('ping', { 'address': remoteAddress, 'count': '1' })

    for ping in pingResult:
        latencyResult = ping['time']
        latency = int(latencyResult.split('ms')[0])

    queues = api.get_resource('/queue/simple')
    
    # Mendapatkan semua queue terlebih dahulu
    all_queues = queues.get()

    for queue in all_queues:
        name = queue['name']
        if neCode in name:
            # Mengambil limitasi bandwidth
            maxLimit = queue['max-limit'].split('/')
            maxUpload = maxLimit[0]
            maxDownload = maxLimit[1]

            # Mengambil traffic saat ini
            traffic = queue['rate'].split('/')
            tUpload = traffic[0]
            tDownload = traffic[1]
            break

    addressLists = api.get_resource('/ip/firewall/address-list').call('print')
    addressList = [q for q in addressLists if q.get('address') == remoteAddress]

    for address in addressList:
        if address['list'] == 'allow':
            status = 'Subscribe'

        else:
            status = 'Suspend'

    result = {
        'status':status,
        'maxUpload':int(maxUpload)/1000000,
        'maxDownload':int(maxDownload)/1000000,
        'tUpload':int(tUpload)/1000000,
        'tDownload':int(tDownload)/1000000,
        'latency':latency,
    }

    connection.disconnect()

    return result

print(json.dumps(get_traffic_data(), indent=4))