from cryptography.fernet import Fernet
from django.conf import settings

def decryptor(password):
	key = settings.ENCRYPTION_KEY
	cipher_suite = Fernet(key)
	encrypted_data = b'{}'.format(password)
	decrypted_data = cipher_suite.decrypt(encrypted_data)
	
	return decrypted_data