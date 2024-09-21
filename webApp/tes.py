from common import oidLib
import asyncio
from puresnmp import Client, V2C, PyWrapper
import json

def getDataOlt(oltIp, community, oltPort, onuPort):
    async def snmpGet(oltIp, community,oid):
        client = PyWrapper(Client(oltIp, V2C(community)))
        output = await client.get(oid)

        return output

    oidDict = {
            'STATE': str(oidLib.oidOnu['STATE']) + str(oidLib.oidPortAll['port'][oltPort]['OID']) + '.' + str(onuPort),
            'REDAMAN': str(oidLib.oidOnu['REDAMAN']) + str(oidLib.oidPortAll['port'][oltPort]['OID']) + '.' + str(onuPort) + '.1',
            'AUTHPASS': str(oidLib.oidOnu['AUTHPASS']) + str(oidLib.oidPortAll['port'][oltPort]['OID']) + '.' + str(onuPort),
            'OFFLINE': str(oidLib.oidOnu['OFFLINE']) + str(oidLib.oidPortAll['port'][oltPort]['OID']) + '.' + str(onuPort),
            'TYPE': str(oidLib.oidOnu['TYPE']) + str(oidLib.oidPortAll['port'][oltPort]['OID']) + '.' + str(onuPort),
            'NAME': str(oidLib.oidOnu['NAME']) + str(oidLib.oidPortAll['port'][oltPort]['OID']) + '.' + str(onuPort),
            'SN': str(oidLib.oidOnu['SN']) + str(oidLib.oidPortAll['port'][oltPort]['OID']) + '.' + str(onuPort),
            'SSID' : "1.3.6.1.4.1.3902.1012.3.28.1.1.5.268501248.1",
#            'PASSWORD' : "1.3.6.1.4.1.3902.1012.3.13.3.1.5.268501248.1",
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
    getSsid = asyncio.run(snmpGet(oltIp, community, oidDict['SSID']))
#    getPassword = asyncio.run(snmpGet(oltIp, community, oidDict['PASSWORD']))

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
            'serialNumber': serialNumberPatern + str(getOnuSn.hex()[8:]).upper(),
            'ssid' : str(getSsid.decode('ISO-8859-1')),
#            'password' : str(getPassword),
        }
    
    return result

output = getDataOlt('172.16.1.106', 'intbnet', '1', 1)

print(json.dumps(output, indent=4))