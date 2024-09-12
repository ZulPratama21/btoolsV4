BtoolsV4 With Django

1. Update dan upgrade repository :
     apt update
     apt upgrade
2. Instal python pip : apt install python3-pip
3. Buat virtual environment : python3 -m venv env
4. Masuk kedalam virtual environemt : source env/bin/activate
5. Install semua library sesuai requirement : pip install -r requirements.txt
6. Struktur direktory:
/root                # Direktori utama
  /webApp            # Direktori project
  /env               # Virtual environment
  /requirement.txt   # List library yang perlu diinstal
7. Jika dalam pengeditan terdapat instalasi library baru, gunakan command berikut agar requirement.txt dapat langsung ter-update : pip install (nama library) && pip freeze > requirements.txt
8. install mysql dengan commanf "apt instaall mysql-server" berikan password ****
9. intall library untuk mengkoneksikan sql dengan django dengan command "apt install python3-dev libmysqlclient-dev"
10. Edit file settings.py didalam direktory /webApp/btools/settings.py pada baris ALLOWED_HOSTS = [] dengan mengedit ip address yang akan digunakan untuk mengakses server : ALLOWED_HOSTS = [<IP Address>]
11. Server sudah siap untuk dijalankan : python3 manage.py runserver <IP Address>:<Port Address>
