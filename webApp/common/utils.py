from cryptography.fernet import Fernet
from django.conf import settings
import routeros_api

def decryptor(password):
	key = settings.ENCRYPTION_KEY
	cipherSuite = Fernet(key)
	encryptedPassword = b'{}'.format(password)
	decryptedPassword = cipherSuite.decrypt(encryptedPassword)
	
	return decryptedPassword