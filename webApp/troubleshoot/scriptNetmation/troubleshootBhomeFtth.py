from routeros_api import RouterOsApiPool
from common import oidLib
from common.oidLib import dictOltIp # Perlu diganti ke database
from common.genieacsApi import getOnuType, zte1, zte2, cdt1, cdt2, cdt3
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

def getAllData(idLoc):
    hostList = ['103.73.72.182', '103.73.72.162', '103.73.72.222'] #Perlu dirubah ke database
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
            'neCode': 'X',
            'clientIp': 'X',
            'comment': 'X',
        }
    
    neCode = (dataRouter['neCode'])
    oltIp = dictOltIp[neCode[:-4]] # perlu dirubah ke database
    oltPort = neCode[-4:-2]
    onuPort = int(neCode[-2:])

    try:
        dataOlt = getDataOlt(oltIp,'intbnet',oltPort,onuPort)

    except Exception as e:
        dataOlt = {
                'state': 'Error',
                'redaman' : 'X',
                'authpass': 'X',
                'offline': 'X',
                'type': 'X',
                'name': 'X',
                'serialNumber': 'X',
            }
    
    onuApi = None
    onuApi = getOnuType.getOnuType(dataRouter['clientIp'])

    if onuApi is None:
        dataOnu = {
            'deviceId':'X',
            'ssid':{
                '5.8':'X',
                '2.4':'X',
            },
            'passWifi':{
                '5.8':'X',
                '2.4':'X'
            },
            'connectedDevice':[
                {
                    'hostName':'X',
                    'ipAddress':'X',
                    'macAddress':'X',
                }
            ],
            'totalConnDevice':'X'
        }

    else:
        dataOnu = None
        
        if onuApi['onuType'] == 'F670L' or onuApi['onuType'] == 'F679':
            dataOnu = zte1.getData(onuApi['deviceId'])

        elif onuApi['onuType'] == 'F609' or onuApi['onuType'] == 'F660':
            dataOnu = zte2.getData(onuApi['deviceId'])

        elif onuApi['onuType'] == 'FD514GD-R460':
            dataOnu = cdt1.getData(onuApi['deviceId'])

        elif onuApi['onuType'] == 'FD514GS1-R550':
            dataOnu = cdt2.getData(onuApi['deviceId'])

        elif onuApi['onuType'] == 'FD512XW-R460':
            dataOnu = cdt3.getData(onuApi['deviceId'])

        if dataOnu is None:
            dataOnu = {
                'deviceId':'X',
                'ssid':{
                    '5.8':'X',
                    '2.4':'X',
                },
                'passWifi':{
                    '5.8':'X',
                    '2.4':'X'
                },
                'connectedDevice':[
                    {
                        'hostName':'X',
                        'ipAddress':'X',
                        'macAddress':'X',
                    }
                ],
                'totalConnDevice':'X'
            }

    dataAll = {**dataRouter, **dataOlt, **dataOnu}

    return dataAll