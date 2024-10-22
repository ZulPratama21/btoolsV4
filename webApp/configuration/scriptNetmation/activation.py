from common.utils import confRouterOs
from datetime import datetime
import time

def deviceActivation(ipDevice, user, password, portSsh, identity, pop, routerFirewall):
    # Mendapatkan waktu saat ini
    currentTime = time.strftime("%H:%M:%S")
    currentDate = datetime.now()
    formattedDate = currentDate.strftime("%b/%d/%Y")


    # Konfigurasi yang bersifat harus memasukan variable dan perlu di eksekusi diawal
    setIdentity = f'/system identity set name="{identity}"'
    addUser = f'/user add name={user} password={password} group=write'
    setClock = f'/system clock set date={formattedDate} time={currentTime} time-zone-autodetect=yes time-zone-name=Asia/Jakart'
    setLog = f'/system logging action add name=syslog remote=172.16.1.61 remote-port=5151 src-address={ipDevice} target=remote'
    startConfig = [setIdentity, addUser, setClock, setLog]

    if routerFirewall == 'yes':
        # Membaca file konfigurasi dan memasukannya kedalam sebuah list
        with open("/root/webApp/scriptNetmation/configureDeviceCoreDistri/activationConfig.txt", "r") as file:
            inputConfig = file.readlines()

    else:
        # Membaca file konfigurasi dan memasukannya kedalam sebuah list
        with open("/root/webApp/scriptNetmation/configureDeviceCoreDistri/activationConfigFirewall.txt", "r") as file:
            inputConfig = file.readlines()

    # Konfigurasi yang bersifat harus memasukan variable dan perlu di eksekusi diakhir
    setIpService = f'/ip service set ssh address=172.16.1.77/32,172.16.1.27/32,172.16.1.50/32,172.16.1.130/32,103.73.74.15/32 port={portDevice}'
    setSnmp = f'/snmp set contact=noc@bnet.id enabled=yes location="{pop}" trap-community=intbnet trap-version=3'
    endConfig = [setIpService, setSnmp]

    # Menggabungkan startConfig dan inputConfig
    configList = startConfig + inputConfig + endConfig

    output = confRouterOs(
        ipDevice,
        user,
        password,
        portSsh,
        'Aktivasi Perangkat BNET',
        configList,
        'y')
    
    return output