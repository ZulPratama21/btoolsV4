
def gConfC320OnuBridge(sn,neCode,ipAddress,subnetMask,limitasi,modemType):
    oltId = int(neCode[-4:-2])
    if oltId < 17:
        oltPort = f'1/1/{oltId}'

    else:
        oltId2 = oltId - 16
        oltPort = f'1/2/{oltId2}'

    vlan = neCode[:-2]
    onu = int(neCode[-2:])

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


def gConfC320OnuPppoe(sn,neCode,limitasi,modemType):
    oltId = int(neCode[-4:-2])
    if neCode[:-4] == '3':
        oltPort = f'1/2/{oltId}'
    
    elif oltId < 17:
        oltPort = f'1/1/{oltId}'

    else:
        oltId2 = oltId - 16
        oltPort = f'1/2/{oltId2}'

    vlan = neCode[:-2]
    onu = int(neCode[-2:])

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
pppoe 1 nat enable user {neCode}@bnethome password bnet{neCode}
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
wan-ip 1 mode pppoe username {neCode}@bnethome password bnet{neCode} vlan-profile vlan{vlan} host 1
wan-ip 1 ping-response enable traceroute-response enable
security-mgmt 1 state enable mode forward protocol web
wan 1 ethuni 1 ssid 1 service tr069 internet host 1
tr069-mgmt 1 acs http://172.16.1.186:7547 validate basic username admin password TR09Bnet137 state unlock
exit'''
        
    return result