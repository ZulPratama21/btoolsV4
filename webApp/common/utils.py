from cryptography.fernet import Fernet
from django.conf import settings
import routeros_api

def decryptor(password):
	key = settings.ENCRYPTION_KEY
	cipherSuite = Fernet(key)
	encryptedPassword = b'{}'.format(password)
	decryptedPassword = cipherSuite.decrypt(encryptedPassword)
	
	return decryptedPassword

def RouterOsGetApi(remoteAddress, userInput, passInput, portInput, parameter):
    api = routeros_api.RouterOsApiPool(
        host=remoteAddress,
        username=userInput,
        password=passInput,
        port=int(portInput),
        plaintext_login=True
    )

    try:
        connection = api.get_api()
        resource = connection.get_resource(parameter)
        action = resource.get()

        return action

    except routeros_api.exceptions.RouterOsApiConnectionError as e:
        return(f'RouterOsApiConnectionError occurred!: {e}')

    except Exception as e:
        return(f'An unexpected exception occurred!: {e}')
         
    finally:
        api.disconnect()

def RouterOsPingApi(remoteAddress, userInput, passInput, portInput, targetIp):
    api = routeros_api.RouterOsApiPool(
        host=remoteAddress,
        username=userInput,
        password=passInput,
        port=int(portInput),
        plaintext_login=True
    )

    try:
        connection = api.get_api()

        result = connection.get_resource('/').call('ping', { 'address': targetIp, 'count': '1' })

        return result

    except routeros_api.exceptions.RouterOsApiConnectionError as e:
        return(f'RouterOsApiConnectionError occurred!: {e}')

    except Exception as e:
        return(f'An unexpected exception occurred!: {e}')

    finally:
        api.disconnect()
        
def RouterOsTrafficApi(remoteAddress, userInput, passInput, portInput, interfaceInput):
    api = routeros_api.RouterOsApiPool(
        host=remoteAddress,
        username=userInput,
        password=passInput,
        port=int(portInput),
        plaintext_login=True  
    )

    try:
        connection = api.get_api()

        result = connection.get_resource('/interface').call('monitor-traffic', { 'interface': interfaceInput, 'duration': '1s' })

        return result

    except routeros_api.exceptions.RouterOsApiConnectionError as e:
        return(f'RouterOsApiConnectionError occurred!: {e}')

    except Exception as e:
        return(f'An unexpected exception occurred!: {e}')

    finally:
        api.disconnect()