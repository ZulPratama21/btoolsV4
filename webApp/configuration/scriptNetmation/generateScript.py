def gConfC320OnuBridge(sn,neCodeMain,ipAddress,subnetMask,limitasi,modemType):
    oltId = int(neCodeMain[-4:-2])
    if neCodeMain[:-4] == '3':
        if oltId < 17:
            oltPort = f'1/2/{oltId}'

        elif oltId < 33:
            oltId2 = oltId - 32
            oltPort = f'1/2/{oltId2}'

    elif oltId < 17:
        oltPort = f'1/1/{oltId}'

    elif oltId < 33:
        oltId2 = oltId - 16
        oltPort = f'1/2/{oltId2}'

    elif oltId < 49:
        oltId2 = oltId - 32
        oltPort = f'1/1/{oltId2}'

    else:
        oltId2 = oltId - 48
        oltPort = f'1/2/{oltId2}'

    vlan = neCodeMain[:-2]
    onu = int(neCodeMain[-2:])

    result = f'''interface gpon-olt_{oltPort}
onu {onu} type {modemType} sn {sn}
exit
interface gpon-onu_{oltPort}:{onu}
sn-bind enable sn
tcont 1 name ip{vlan} profile {limitasi}
gemport 1 name ip{vlan} tcont 1
gemport 1 traffic-limit upstream U-{limitasi} downstream D-{limitasi}
service-port 1 vport 1 user-vlan {vlan} vlan {vlan}
exit
pon-onu-mng gpon-onu_{oltPort}:{onu}
firewall enable level low
service ip{vlan} gemport 1 vlan {vlan}
wan-ip 1 mode static ip-profile ip{vlan} ip-address {ipAddress} mask {subnetMask} vlan-profile vlan{vlan} host 1
vlan port eth_0/1 mode tag vlan {vlan}
security-mgmt 1 state enable mode forward protocol web
tr069-mgmt 1 acs http://172.16.1.186:7547 validate basic username admin password TR09Bnet137 state unlock
exit'''
    
    return result


def gConfC320OnuPppoe(sn,neCodeMain,limitasi,modemType):
    oltId = int(neCodeMain[-4:-2])
    if neCodeMain[:-4] == '3':
        oltPort = f'1/2/{oltId}'
    
    elif oltId < 17:
        oltPort = f'1/1/{oltId}'

    else:
        oltId2 = oltId - 16
        oltPort = f'1/2/{oltId2}'

    vlan = neCodeMain[:-2]
    onu = int(neCodeMain[-2:])

    if modemType == "ZTE-F660":
        result = f'''interface gpon-olt_{oltPort}
onu {onu} type {modemType} sn {sn}
exit
interface gpon-onu_{oltPort}:{onu}
sn-bind enable sn
tcont 1 name pppoenat profile {limitasi}
gemport 1 name pppoenat tcont 1
gemport 1 traffic-limit upstream U-{limitasi} downstream D-{limitasi}
service-port 1 vport 1 user-vlan {vlan} vlan {vlan}
exit
pon-onu-mng gpon-onu_{oltPort}:{onu}
firewall enable level low
service pppoenat gemport 1 vlan {vlan}
pppoe 1 nat enable user {neCodeMain}@bnethome password bnet{neCodeMain}
security-mgmt 1 state enable mode forward protocol web
tr069-mgmt 1 acs http://172.16.1.186:7547 validate basic username admin password TR09Bnet137 state unlock
exit'''
    
    else:
        result = f'''interface gpon-olt_{oltPort}
onu {onu} type {modemType} sn {sn}
exit
interface gpon-onu_{oltPort}:{onu}
sn-bind enable sn
tcont 1 name pppoenat profile {limitasi}
gemport 1 name pppoenat tcont 1
gemport 1 traffic-limit upstream U-{limitasi} downstream D-{limitasi}
service-port 1 vport 1 user-vlan {vlan} vlan {vlan}
exit
pon-onu-mng gpon-onu_{oltPort}:{onu}
firewall enable level low
service pppoenat gemport 1 vlan {vlan}
wan-ip 1 mode pppoe username {neCodeMain}@bnethome password bnet{neCodeMain} vlan-profile vlan{vlan} host 1
wan-ip 1 ping-response enable traceroute-response enable
security-mgmt 1 state enable mode forward protocol web
wan 1 ethuni 1 ssid 1 service tr069 internet host 1
tr069-mgmt 1 acs http://172.16.1.186:7547 validate basic username admin password TR09Bnet137 state unlock
exit'''
        
    return result

def createGateway(ipAddress):
    octets = ipAddress.split('.')
    octets[-1] = str(int(octets[-1]) - 1)
    gateway = '.'.join(octets)

    return gateway

def gConfC320OnuStatic(sn,neCodeMain,ipAddress,subnetMask,limitasi,modemType):
    gateway = createGateway(ipAddress)
    oltId = int(neCodeMain[-4:-2])
    if neCodeMain[:-4] == '3':
        if oltId < 17:
            oltPort = f'1/2/{oltId}'

        elif oltId < 33:
            oltId2 = oltId - 32
            oltPort = f'1/2/{oltId2}'

    elif oltId < 17:
        oltPort = f'1/1/{oltId}'

    elif oltId < 33:
        oltId2 = oltId - 16
        oltPort = f'1/2/{oltId2}'

    elif oltId < 49:
        oltId2 = oltId - 32
        oltPort = f'1/1/{oltId2}'

    else:
        oltId2 = oltId - 48
        oltPort = f'1/2/{oltId2}'

    vlan = neCodeMain[:-2]
    onu = int(neCodeMain[-2:])

    result = f'''gpon
onu profile ip {sn} gateway {gateway} primary-dns 103.73.73.71 second-dns 103.73.73.72
exit
interface gpon-olt_{oltPort}
onu {onu} type {modemType} sn {sn}
exit
interface gpon-onu_{oltPort}:{onu}
sn-bind enable sn
tcont 1 name ip{vlan} profile {limitasi}
gemport 1 name ip{vlan} tcont 1
service-port 1 vport 1 user-vlan {vlan} vlan {vlan}
exit
pon-onu-mng gpon-onu_{oltPort}:{onu}
firewall enable level low
service ip{vlan} gemport 1 vlan {vlan}
wan-ip 1 mode static ip-profile {sn} ip-address {ipAddress} mask {subnetMask} vlan-profile vlan{vlan} host 1
security-mgmt 1 state enable mode forward protocol web
tr069-mgmt 1 acs http://172.16.1.186:7547 validate basic username admin password TR09Bnet137 state unlock
exit'''

    return result

def gConfC320OnuManyPacket(vlanGw, sn,neCodes,ipAddress,limitasi,modemType):
    neCodeMain = neCodes[0]
    oltId = int(neCodeMain[-4:-2])

    if neCodeMain[:-4] == '3':
        if oltId < 17:
            oltPort = f'1/2/{oltId}'
        elif oltId < 33:
            oltId2 = oltId - 32
            oltPort = f'1/2/{oltId2}'
    elif oltId < 17:
        oltPort = f'1/1/{oltId}'
    elif oltId < 33:
        oltId2 = oltId - 16
        oltPort = f'1/2/{oltId2}'
    elif oltId < 49:
        oltId2 = oltId - 32
        oltPort = f'1/1/{oltId2}'
    else:
        oltId2 = oltId - 48
        oltPort = f'1/2/{oltId2}'

    onu = int(neCodeMain[-2:])

    vlans = {}
    tconts = {}
    gemports = {}
    servicePorts = {}
    services = {}
    vlanTags = {}

    for x in range(1, len(neCodes) + 1):
        vlanForward = neCodes[x-1][:-2]
        vlans[x] = vlanForward
        tconts[x] = f'tcont {x} name ip{vlans[x]} profile {limitasi}'
        gemports[x] = f'gemport {x} name ip{vlans[x]} tcont {x}'
        servicePorts[x] = f'service-port {x} vport {x} user-vlan {vlans[x]} vlan {vlans[x]}'
        services[x] = f'service ip{vlans[x]} gemport {x} vlan {vlans[x]}'
        vlanTags[x] = f'vlan port eth_0/{x} mode tag vlan {vlans[x]}'

    tconts_str = '\n'.join([tconts[x] for x in range(1, len(tconts) + 1)])
    gemports_str = '\n'.join([gemports[x] for x in range(1, len(gemports) + 1)])
    servicePorts_str = '\n'.join([servicePorts[x] for x in range(1, len(servicePorts) + 1)])
    services_str = '\n'.join([services[x] for x in range(1, len(services) + 1)])
    vlanTags_str = '\n'.join([vlanTags[x] for x in range(1, len(vlanTags) + 1)])

    result = f'''interface gpon-olt_{oltPort}
onu {onu} type {modemType} sn {sn}
exit
interface gpon-onu_{oltPort}:{onu}
sn-bind enable sn
{tconts_str}
{gemports_str}
{servicePorts_str}
exit
pon-onu-mng gpon-onu_{oltPort}:{onu}
{services_str}
wan-ip 1 mode static ip-profile ip{vlanGw} ip-address {ipAddress} mask 255.255.255.0 vlan-profile vlan{vlanGw} host 1
{vlanTags_str}
tr069-mgmt 1 acs http://172.16.1.186:7547 validate basic username admin password TR09Bnet137 state unlock
exit'''
    
    return result