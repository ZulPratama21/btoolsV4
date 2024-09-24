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

    queues = api.get_resource('/queue/simple')
    allQueue = queues.get(name=idLoc)
    queue = allQueue[0]

    clientIp = queue['target'].split('/')[0]
    clientName = queue['comment']
    maxLimit = queue['max-limit'].split('/')
    maxUpload = int(maxLimit[0])/1000000
    maxDownload = int(maxLimit[1])/1000000

    traffic = queue['rate'].split('/')
    tUpload = int(traffic[0])/1000000
    tDownload = int(traffic[1])/1000000

    # Mengambil latency
    pingResult = api.get_resource('/').call('ping', { 'address': clientIp, 'count': '1', 'interval':'0.1s' })
    ping = pingResult[0]
    
    if 'time' in ping:
        latencyResult = ping['time']
        if 'ms' in latencyResult:
            latency = int(latencyResult.split('ms')[0])
        else:
            latency = 0
    else:
        latency = 'X'
    
    # Mengambil status client
    addressLists = api.get_resource('/ip/firewall/address-list')
    addressList_List = addressLists.get(address=clientIp)
    addressList = addressList_List[0]

    if addressList['list'] == 'allow':
        status = 'Subscribe'
    else:
        status = 'Suspend'
    
    result = {
        'statusClient':status,
        'maxUpload':maxUpload,
        'maxDownload':maxDownload,
        'tUpload':tUpload,
        'tDownload':tDownload,
        'latency':latency,
        'clientIp':clientIp,
        'name':clientName,
    }
    connection.disconnect()

    return result

def getAllData(idLoc):
    hostList = ['103.73.72.72', '103.73.72.73', '103.73.72.74'] #Perlu dirubah ke database
    dataRouter = None

    for host in hostList:
        try:
            dataRouter = getDataRouter(idLoc, host, 'neteng', 'netEngineerBnet', '8728') #Akses user masih static, harus ambil dari database
            
        except Exception as e:
            continue

    if dataRouter is None:
        return {
            'statusClient': 'Null',
            'maxUpload': 'X',
            'maxDownload': 'X',
            'tUpload': 'X',
            'tDownload': 'X',
            'latency': 'X',
            'clientIp': 'X',
            'clientName': 'X',
        }

    return dataRouter