from cryptography.fernet import Fernet
from django.conf import settings
import paramiko
import datetime
import time

def decryptor(password):
    key = settings.ENCRYPTION_KEY
    cipherSuite = Fernet(key)
    
    if isinstance(password, str):
        encryptedPassword = password.encode()
    else:
        encryptedPassword = password
    
    decryptedPassword = cipherSuite.decrypt(encryptedPassword)
    
    return decryptedPassword.decode()

def writeLog(remoteAddress, user, activity, log):
	currentTime = datetime.datetime.now()
	formattedTime = currentTime.strftime("%d/%m/%Y %H:%M:%S")
	logOutput = f'\n{formattedTime} || {remoteAddress} || {user} || {activity} || {log}'

	with open('common/log.txt','a') as f:
		f.write(logOutput)

	if 'password' in logOutput:
		logOutput = f'\n{formattedTime} || {remoteAddress} || {user} || {activity}'

	return logOutput

def confRouterOs(remoteAddress, user, password, port, activity, configList, rollBack):
	successConf = 0
	logList = []

	try:
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(hostname=remoteAddress,username=user,password=password,port=port)

		log = writeLog(remoteAddress, user, activity, f'Berhasil login pada perangkat {remoteAddress}')
		logList.append(log)

		for config in configList:
			stdin, stdout, stderr = ssh_client.exec_command(config)
			time.sleep(0.5)

			output = (stdout.read().decode("ascii").strip("\n"))

			if(len(output) != 0):
				log = writeLog(remoteAddress, user, activity, f'terjadi error pada konfigurasi: {config} dengan detail: {output}')
				logList.append(log)
				
				if rollBack == 'y':
					for x in range(successConf):
						ssh_client.exec_command('undo')
					
					break
				
				else:
					continue

			else:
				log = writeLog(remoteAddress, user, activity, f'Berhasil melakukan konfigurasi: {config}')
				logList.append(log)

				successConf += 1

	except Exception as e:
		log = writeLog(remoteAddress, user, activity, f'Terjadi kegagalan login pada perangkat {remoteAddress} dengan detail : {e}')
		logList.append(log)

	return logList