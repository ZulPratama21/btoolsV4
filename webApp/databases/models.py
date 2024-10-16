from django.db import models

# Create your models here.

class UserDevice(models.Model):
	user	= models.CharField(
		max_length = 100,
		default = 'admin',
		)
	
	password		= models.CharField(max_length = 1000)
	
	listGroup = (
		('Read','read'),
		('Write','Write'),
		('Full','full'),
		)

	group	= models.CharField(
		max_length = 100,
		choices = listGroup,
		default = 'read',
		)
	
	published	= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)

	def __str__(self):
		return "{}. {}".format(self.id,self.user)
	
class Client(models.Model):
    idpelanggan = models.CharField(max_length = 10)
    necode = models.CharField(max_length = 15)
    namapelanggan = models.CharField(max_length = 255)
    tanggalinstalasi = models.DateField()
    ipremote = models.CharField(max_length = 20)
    portwinbox = models.IntegerField(blank=True, null=True)
    portssh = models.IntegerField(blank=True, null=True)
    portapi = models.IntegerField(blank=True, null=True)
    portweb = models.IntegerField(blank=True, null=True)
    iplinkmain = models.CharField(max_length = 100)
    iplinkbackup = models.CharField(max_length = 100)
    iptambahan = models.TextField(blank=True, null=True)

    # Perlu ganti ke select field sesuai database perangkat
    parentrouter = models.CharField(max_length = 255)

    listPaket = (
        ('Dedicated', 'dedicated'),
        ('Upto', 'upto'),
        ('Bhome', 'bhome'),
        ('Konekyu', 'konekyu'),
    )

    jenispaket = models.CharField(
		max_length = 100,
		choices = listPaket,
		default = 'bhome',
		)

    bwupload = models.FloatField()
    bwdownload = models.FloatField()

    listAktivasiBtools = (
        ('Ya', 'ya'),
        ('Tidak', 'tidak'),
        ('Tidak Ada Akses', 'tidak ada akses'),
        ('Perangkat Milik Client', 'perangkat milik client'),
    )

    aktivasibtools = models.CharField(
		max_length = 100,
		choices = listAktivasiBtools,
		default = 'tidak',
		)

    # harus diganti menggunakan database perangkat
    connectto = models.CharField(max_length = 100)

    onuid = models.IntegerField(blank=True, null=True)
    portconnect = models.IntegerField(blank=True, null=True)

    # Perlu diganti ke select field database POP
    pop = models.CharField(max_length = 255)

    listBiner = (
        ('Ya', 'ya'),
        ('Tidak', 'tidak')
    )

    mrtg = models.CharField(
		max_length = 100,
		choices = listBiner,
		default = 'tidak',
		)

    nagios = models.CharField(
		max_length = 100,
		choices = listBiner,
		default = 'tidak',
		)

    smokeping = models.CharField(
		max_length = 100,
		choices = listBiner,
		default = 'tidak',
		)

    listMedia = (
        ('Converter/SFP', 'converter/sfp'),
        ('ODP', 'odp'),
        ('LAN', 'lan'),
        ('Wireless', 'wireless'),
    )

    media = models.CharField(
		max_length = 100,
		choices = listMedia,
		default = 'tidak',
		)

    redamansignalawal = models.CharField(max_length = 10)
    remark = models.TextField(blank=True, null=True)

    updated	= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}. {self.idpelanggan} - {self.necode} - {self.namapelanggan}'
        
class Odp(models.Model):
  odpId = models.CharField(max_length = 100)
  tanggalinstalasi = models.DateField()
  portFilled = models.IntegerField()
  portRemaining = models.IntegerField(default=16)
  total_port = models.IntegerField(default=16)
  portOlt = models.CharField(max_length = 10)
  oltIp = models.CharField(max_length = 20)
  identityOlt = models.CharField(max_length = 100)
  segmen = models.CharField(max_length = 100)
  tikor = models.CharField(max_length = 255)
  alamat = models.TextField()

  opname = (
    ('Done','done'),
    ('-','-'),
  )

  statusOpname = models.CharField(
		max_length = 100,
		choices = opname,
		default = '-',
		)

  remark = models.TextField(blank=True, null=True)

  updated	= models.DateTimeField(auto_now=True)

  def __str__(self):
      return f'{self.id}. {self.odpId} - {self.segmen}'