from databases.models import UserDevice
from common.utils import confRouterOs, decryptor
from datetime import datetime
import time

def deviceActivationRos(remoteAddress, user, password, portSsh, deviceId, pop, routerFirewall):
    # Mengatur Hak Akses
    removeUserAdmin = '/user remove admin'
    addActivator = f'/user add name={user} password={password} group=write'
    superUser = UserDevice.objects.get(user='bnettools')
    addSuperUser = f'/user add name={superUser.user} password={decryptor(superUser.password)} group=full address=172.16.1.27/32,172.16.1.130/32'
    configUser = [removeUserAdmin, addActivator,addSuperUser]
    
    output = confRouterOs(
        remoteAddress,
        'admin',
        '',
        22,
        'Aktivasi Perangkat BNET',
        configUser,
        'n')

    # Mendapatkan waktu saat ini
    currentTime = time.strftime("%H:%M:%S")
    currentDate = datetime.now()
    formattedDate = currentDate.strftime("%b/%d/%Y")

    # Konfigurasi yang bersifat harus memasukan variable dan perlu di eksekusi diawal
    setIdentity = f'/system identity set name="{deviceId}"'
    setClock = f'/system clock set date={formattedDate} time={currentTime} time-zone-autodetect=yes time-zone-name=Asia/Jakart'
    setLog = f'/system logging action add name=syslog remote=172.16.1.61 remote-port=5151 src-address={remoteAddress} target=remote'
    startConfig = [setIdentity, setClock, setLog]

    if routerFirewall.lower() == 'ya':
        # Membaca file konfigurasi dan memasukannya kedalam sebuah list
        with open("configuration/scriptNetmation/activationConfigFirewall.txt", "r") as file:
            inputConfig = file.readlines()

    else:
        # Membaca file konfigurasi dan memasukannya kedalam sebuah list
        with open("configuration/scriptNetmation/activationConfig.txt", "r") as file:
            inputConfig = file.readlines()

    # Konfigurasi yang bersifat harus memasukan variable dan perlu di eksekusi diakhir
    setIpService = f'/ip service set ssh address=172.16.1.77/32,172.16.1.27/32,172.16.1.50/32,172.16.1.130/32,103.73.74.15/32 port={portSsh}'
    setSnmp = f'/snmp set contact=noc@bnet.id enabled=yes location="{pop}" trap-community=intbnet trap-version=3'
    endConfig = [setIpService, setSnmp]

    # Menggabungkan startConfig dan inputConfig
    configList = startConfig + inputConfig + endConfig

    output = confRouterOs(
        remoteAddress,
        user,
        password,
        22,
        'Aktivasi Perangkat BNET',
        configList,
        'y')
    
    return output