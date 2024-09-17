from cryptography.fernet import Fernet
from django.conf import settings

def decryptor(password):
	key = settings.ENCRYPTION_KEY
	cipherSuite = Fernet(key)
	encryptedPassword = b'{}'.format(password)
	decryptedPassword = cipherSuite.decrypt(encryptedPassword)
	
	return decryptedPassword