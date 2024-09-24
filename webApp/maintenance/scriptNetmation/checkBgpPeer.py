from routeros_api import RouterOsApiPool

def getDataRouter(identity, hostInput, userInput, passwordInput, portInput):
    connection = RouterOsApiPool(
        host=hostInput,
        username=userInput,
        password=passwordInput,
        port=int(portInput),
        plaintext_login=True
    )
    api = connection.get_api()

    version = int(api.get_resource('system/resource/').get()[0]['version'].split('.')[0])
    
    bgpList = []

    if version < 7:
        bgps = api.get_resource('/routing/bgp/peer')
        allBgp = bgps.get()

        for bgp in allBgp:
            if bgp['disabled'] == 'false':
                if bgp['established'] == 'true':
                    bgpList.append({'identity':identity,
                                    'ipDevice':hostInput,
                                    'name':bgp['name'],
                                    'disabled':bgp['disabled'],
                                    'localAddress':bgp['local-address'],
                                    'remoteAddress':bgp['remote-address'],
                                    'remoteId':bgp['remote-id'],
                                    'remoteAs':bgp['remote-as'],
                                    'prefixCount':bgp['prefix-count'],
                                    'established':bgp['established'],
                    })
                else:
                    bgpList.append({'identity':identity,
                                    'ipDevice':hostInput,
                                    'name':bgp['name'],
                                    'disabled':bgp['disabled'],
                                    'localAddress':'X',
                                    'remoteAddress':bgp['remote-address'],
                                    'remoteId':'X',
                                    'remoteAs':bgp['remote-as'],
                                    'prefixCount':'X',
                                    'established':bgp['established'],
                    })

            else:
                bgpList.append({'identity':identity,
                'ipDevice':hostInput,
                'name':bgp['name'],
                'disabled':bgp['disabled'],
                'localAddress':'X',
                'remoteAddress':bgp['remote-address'],
                'remoteId':'X',
                'remoteAs':bgp['remote-as'],
                'prefixCount':'X',
                'established':'X',
                })
    else:

        bgpConns = api.get_resource('/routing/bgp/connection/')
        allBgpConn = bgpConns.get()

        for bgpConn in allBgpConn:
            if bgpConn['disabled'] == 'false':
                if bgpConn['inactive'] == 'false':
                    bgpSessions = api.get_resource('/routing/bgp/session/')
                    getBgpSession = bgpSessions.get(name=bgpConn['name'] + '-1')
                    bgpSession = getBgpSession[0]
                    bgpList.append({'identity':identity,
                                'ipDevice':hostInput,
                                'name':bgpSession['name'],
                                'disabled':'false',
                                'localAddress':bgpSession['local.address'],
                                'remoteAddress':bgpSession['remote.address'],
                                'remoteId':bgpSession['remote.id'],
                                'remoteAs':bgpSession['remote.as'],
                                'prefixCount':bgpSession['prefix-count'],
                                'established':bgpSession['established'],
                                })
                
            else:
                bgpList.append({'identity':identity,
                                'ipDevice':hostInput,
                                'name':bgpConn['name'],
                                'disabled':'true',
                                'localAddress':bgpConn['local.address'],
                                'remoteAddress':bgpConn['remote.address'],
                                'remoteId':'X',
                                'remoteAs':bgpSession['remote.as'],
                                'prefixCount':'X',
                                'established':'X',
                                })
                continue

        connection.disconnect()

    return bgpList

def getBgpList(bgpDevices):
    bgpList = []
    for device in bgpDevices:
        try:
            dataPeer = getDataRouter('identity',device, 'jul', 'Juliandi123!@#', 8728)
            for peer in dataPeer:
                bgpList.append(peer)
        except Exception:
            bgpList.append({'identity':'identity',
                            'ipDevice':device,
                            'name':'X',
                            'disabled':'X',
                            'localAddress':'X',
                            'remoteAddress':'X',
                            'remoteId':'X',
                            'remoteAs':'X',
                            'prefixCount':'X',
                            'established':'X',
            })

    return bgpList