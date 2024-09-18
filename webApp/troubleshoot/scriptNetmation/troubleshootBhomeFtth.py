from routeros_api import RouterOsApiPool

def getDataRouter(inputIdLoc, hostInput, userInput, passwordInput, portInput):
    idLoc = inputIdLoc.upper()

    connection = RouterOsApiPool(
        host=hostInput,
        username=userInput,
        password=passwordInput,
        port=int(portInput),
        plaintext_login=True
    )
    api = connection.get_api()

    secrets = api.get_resource('/ppp/secret')
    allSecret = secrets.get()

    for secret in allSecret:
        comment = secret['comment']
        if idLoc in comment:
            # Mengambil Kode NE untuk kebutuhan troubleshoot
            commentId = comment.split()[0]
            neCode = commentId.split('-')[1]

            # Mengambil ip address client untuk melakukan ping
            remoteAddress = secret['remote-address']
            break

    # Mengambil latency
    pingResult = api.get_resource('/').call('ping', { 'address': remoteAddress, 'count': '1' })
    for ping in pingResult:
        latencyResult = ping['time']
        if 'ms' in latencyResult:
            latency = int(latencyResult.split('ms')[0])
        else:
            latency = 0

    # Mendapatkan semua queue terlebih dahulu
    queues = api.get_resource('/queue/simple')
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

    # Mengambil status client
    addressLists = api.get_resource('/ip/firewall/address-list').call('print')
    addressList = [q for q in addressLists if q.get('address') == remoteAddress]

    for address in addressList:
        if address['list'] == 'allow':
            status = 'Subscribe'
        else:
            status = 'Suspend'

    result = {
        'statusClient':status,
        'maxUpload':int(maxUpload)/1000000,
        'maxDownload':int(maxDownload)/1000000,
        'tUpload':int(tUpload)/1000000,
        'tDownload':int(tDownload)/1000000,
        'latency':latency,
    }

    connection.disconnect()

    return result
