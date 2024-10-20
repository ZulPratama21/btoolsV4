from routeros_api import RouterOsApiPool
import json

def getNeCode(inputIdLoc, hostInput, userInput, passwordInput, portInput):
    idLoc = inputIdLoc.upper()
    
    connection = RouterOsApiPool(
        host=hostInput,
        username=userInput,
        password=passwordInput,
        port=int(portInput),
        plaintext_login=True
    )
    api = connection.get_api()

    # Mencari secret user
    secrets = api.get_resource('/ppp/secret')
    allSecret = secrets.get()

    for secret in allSecret:
        comment = secret['comment']
        if idLoc in comment:
            # Mengambil Kode NE untuk kebutuhan troubleshoot
            commentId = comment.split()[0]
            neCode = commentId.split('-')[1]
            secretName = f'<pppoe-{secret["name"]}>'
            
            # Mengambil ip address client untuk melakukan ping
            clientIp = secret['remote-address']
            break

    # Mengambil identity parent router
    identityList = api.get_resource('/system/identity').get()
    identity = identityList[0]['name']

    # Identity router
    rhDict = {
        'RTR-B_RH-POP001-001-A202':'103.73.72.182',
        'RTR-B_RH-POP001-002-A202':'103.73.72.162',
        'RTR-B_RH-POP001-003-A202':'103.73.72.222',
    }

    ipHost = rhDict[identity]

    result = {
        'comment': comment,
        'neCode': neCode,
        'secretName': secretName,
        'clientIp': clientIp,
        'identity': identity,
        'ipHost': ipHost,
    }

    return result

def getDataRouter(hostInput, userInput, passwordInput, portInput, comment, clientIp, identity):
    idLoc = inputIdLoc.upper()
    
    connection = RouterOsApiPool(
        host=hostInput,
        username=userInput,
        password=passwordInput,
        port=int(portInput),
        plaintext_login=True
    )
    api = connection.get_api()

    # Mengambil latency
    pingResult = api.get_resource('/').call('ping', { 'address': clientIp, 'count': '1', 'interval':'0.1s' })
    ping = pingResult[0]
    
    if 'time' in ping:
        latencyResult = ping['time']
        if 'ms' in latencyResult:
            latency = int(latencyResult.split('ms')[0])
        else:
            latency = 0

    elif ping['status'] == 'timeout':
        latency = 'timeout'

    else:
        latency = 'X'
    
    # Mendapatkan semua queue terlebih dahulu
    queues = api.get_resource('/queue/simple')
    queueList = queues.get(name=secretName)
    
    if queueList == []:
        queueList = queues.get(name=neCode)
        if queueList == []:
            maxUpload = 0
            maxDownload = 0
            tUpload = 0
            tDownload = 0

        else:
            queue = queueList[0]
            
            maxLimit = queue['max-limit'].split('/')
            maxUpload = maxLimit[0]
            maxDownload = maxLimit[1]

            # Mengambil traffic saat ini
            traffic = queue['rate'].split('/')
            tUpload = traffic[0]
            tDownload = traffic[1]
    else:    
        queue = queueList[0]

        maxLimit = queue['max-limit'].split('/')
        maxUpload = maxLimit[0]
        maxDownload = maxLimit[1]

        # Mengambil traffic saat ini
        traffic = queue['rate'].split('/')
        tUpload = traffic[0]
        tDownload = traffic[1]

       
    # Mengambil status client
    addressLists = api.get_resource('/ip/firewall/address-list')
    addressList_List = addressLists.get(address=clientIp, list='allow')
    
    if addressList_List == []:
        status = 'Suspend'

    else:
        status = 'Subscribe'
    
    result = {
        'parentRouter':identity,
        'statusClient':status,
        'maxUpload':int(maxUpload)/1000000,
        'maxDownload':int(maxDownload)/1000000,
        'tUpload':int(tUpload)/1000000,
        'tDownload':int(tDownload)/1000000,
        'latency':latency,
        'neCode':neCode,
        'clientIp':clientIp,
        'comment':comment,
    }
    
    connection.disconnect()

    return result

hostList = ['103.73.72.182', '103.73.72.162', '103.73.72.222'] #Perlu dirubah ke database
paramCheck = None

for host in hostList:
    try:
        paramCheck = getNeCode('CA0083002', host, 'neteng', 'netEngineerBnet', '8728') #Akses user masih static, harus ambil dari database

    except Exception as e:
        continue

if paramCheck is None:
    print(json.dumps({
        'statusClient': 'Null',
        'maxUpload': 'X',
        'maxDownload': 'X',
        'tUpload': 'X',
        'tDownload': 'X',
        'latency': 'X',
        'neCode': 'X',
        'clientIp': 'X',
        'comment': 'X',
    }, indent=4))

else:
    print(json.dumps(paramCheck, indent=4))

output = getDataRouter(paramCheck['ipHost'],
    'neteng',
    'netEngineerBnet',
    8728,
    paramCheck['comment'],
    paramCheck['clientIp'],
    paramCheck['identity'],
    )
    
print(json.dumps(output, indent=4))