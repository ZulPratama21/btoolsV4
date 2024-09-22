from routeros_api import RouterOsApiPool
from common import oidLib
import asyncio
from puresnmp import Client, V2C, PyWrapper

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
            secretName = f'<pppoe-{secret["name"]}>'

            # Mengambil ip address client untuk melakukan ping
            clientIp = secret['remote-address']
            break
    
    # Mengambil latency
    pingResult = api.get_resource('/').call('ping', { 'address': clientIp, 'count': '1', 'interval':'0.1s' })
    for ping in pingResult:
        latencyResult = ping['time']
        if 'ms' in latencyResult:
            latency = int(latencyResult.split('ms')[0])
        else:
            latency = 0

    # Mendapatkan semua queue terlebih dahulu
    queues = api.get_resource('/queue/simple')
    queueList = queues.get(name=secretName)
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
    addressList_List = addressLists.get(address=clientIp)
    addressList = addressList_List[0]

    if addressList['list'] == 'allow':
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
        'neCode':neCode,
        'clientIp':clientIp
    }

    connection.disconnect()

    return result

def getDataOlt(oltIp, community, oltPort, onuPort):
    async def snmpGet(oltIp, community,oid):
        client = PyWrapper(Client(oltIp, V2C(community)))
        output = await client.get(oid)

        return output

    oidDict = {
            'STATE': str(oidLib.oidOnu['STATE']) + str(oidLib.oidPort['port'][oltPort]['OID']) + '.' + str(onuPort),
            'REDAMAN': str(oidLib.oidOnu['REDAMAN']) + str(oidLib.oidPort['port'][oltPort]['OID']) + '.' + str(onuPort) + '.1',
            'AUTHPASS': str(oidLib.oidOnu['AUTHPASS']) + str(oidLib.oidPort['port'][oltPort]['OID']) + '.' + str(onuPort),
            'OFFLINE': str(oidLib.oidOnu['OFFLINE']) + str(oidLib.oidPort['port'][oltPort]['OID']) + '.' + str(onuPort),
            'TYPE': str(oidLib.oidOnu['TYPE']) + str(oidLib.oidPort['port'][oltPort]['OID']) + '.' + str(onuPort),
            'NAME': str(oidLib.oidOnu['NAME']) + str(oidLib.oidPort['port'][oltPort]['OID']) + '.' + str(onuPort),
            'SN': str(oidLib.oidOnu['SN']) + str(oidLib.oidPort['port'][oltPort]['OID']) + '.' + str(onuPort),
        }

    getOnuState = asyncio.run(snmpGet(oltIp, community,oidDict['STATE']))
    getOnuRedaman = asyncio.run(snmpGet(oltIp, community,oidDict['REDAMAN']))
    getOnuRedaman = asyncio.run(snmpGet(oltIp, community,oidDict['REDAMAN'])) * 0.002 - 30
    redamanResult = getOnuRedaman - 131.07 if getOnuRedaman > 90 else getOnuRedaman
    getOnuAuthpass = asyncio.run(snmpGet(oltIp, community, oidDict['AUTHPASS']))
    getOnuOffline = asyncio.run(snmpGet(oltIp, community, oidDict['OFFLINE']))
    getOnuType = asyncio.run(snmpGet(oltIp, community, oidDict['TYPE']))
    getOnuName = asyncio.run(snmpGet(oltIp, community, oidDict['NAME']))
    getOnuSn = asyncio.run(snmpGet(oltIp, community, oidDict['SN']))

    if getOnuState == 0:
        getOnuState = "Logging"
    elif getOnuState == 1:
        getOnuState = "Los"
    elif getOnuState == 2:
        getOnuState = "SynMiB"
    elif getOnuState == 3:
        getOnuState = "Working"
    elif getOnuState == 4:
        getOnuState = "DyingGasp"
    elif getOnuState == 5:
        getOnuState = "AuthFailed"
    elif getOnuState == 6:
        getOnuState = "Offline"

    if str(getOnuType.decode('utf-8')) == "FD514GD-R460":
        serialNumberPatern = "DF18"
    else:
        serialNumberPatern = "ZTEG"

    result = {
            'state': str(getOnuState),
            'redaman' : round(redamanResult, 2),
            'authpass': str(getOnuAuthpass.decode('utf-8')),
            'offline': str(getOnuOffline.decode('utf-8')),
            'type': str(getOnuType.decode('utf-8')),
            'name': str(getOnuName.decode('utf-8')),
            'serialNumber': serialNumberPatern + str(getOnuSn.hex()[8:]).upper()
        }

    return result