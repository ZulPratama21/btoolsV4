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
		('Write','write'),
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
		return f"{self.id}. {self.user} - {self.group}"
	
class Client(models.Model):
    idpelanggan = models.CharField(max_length = 10)
    necode = models.CharField(max_length = 15)
    namapelanggan = models.CharField(max_length = 255)
    tanggalinstalasi = models.DateField()
    ipremote = models.CharField(max_length = 20)
    deviceOs = models.CharField(max_length = 100)
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

class Device(models.Model):
  pop = models.CharField(max_length = 100)
  deviceId = models.CharField(max_length = 100)
  installedDate = models.DateField()
  remoteAddress = models.CharField(max_length = 100)
  addtionalIp = models.CharField(max_length = 100)
  portWinbox = models.IntegerField(default=8291)
  portSsh = models.IntegerField(default=22)
  portApi = models.IntegerField(default=8728)
  portWeb = models.IntegerField(default=80)

  layerList = (
    ('BGP','bgp'),
    ('Core','core'),
    ('QRP','qrp'),
    ('BHome','bhome'),
    ('Konekyu','konekyu'),
    ('Distribution','distribution'),
    ('Access','access'),
  )

  layer = models.CharField(
    max_length = 15,
		choices = layerList,
		default = 'Access',
    )

  routerFirewallChoice = (
    ('Ya','ya'),
    ('Tidak','tidak'),
  )

  routerFirewall = models.CharField(
		max_length = 6,
		choices = routerFirewallChoice,
		default = 'Tidak',
		)


  role = models.CharField(max_length = 100) # perlu diganti menjadi sebuah database
  frequency = models.IntegerField(default=5000) # perlu ditambahkan peraturan yang tidak memperbolehkan freq tertentu

  bandList = (
    ('5Ghz-A','5ghz-a'),
    ('5Ghz-Only-N','5ghz-only-n'),
    ('5Ghz-A/N','5ghz-a/n'),
    ('5Ghz-A/N/AC','5ghz-a/n/ac'),
    ('5Ghz-Only-AC','5ghz-only-ac'),
    ('5Ghz-N/AC','5ghz-n/ac'),
    ('-','-'),
  )

  channelBand = models.CharField(
    max_length = 100,
		choices = bandList,
		default = '-',
    )

  widthList = (
    ('20Mhz','20mhz'),
    ('40Mhz','40mhz'),
    ('80Mhz','80mhz'),
    ('20/40Mhz EC','20/40mhz ec'),
    ('20/40Mhz CE','20/40mhz ce'),
    ('20/40Mhz XX','20/40mhz xx'),
    ('20/40/80Mhz CEEE','20/40/80mhz ceee'),
    ('20/40/80Mhz ECEE','20/40/80mhz ecee'),
    ('20/40/80Mhz EECE','20/40/80mhz eece'),
    ('20/40/80Mhz EEEC','20/40/80mhz eeec'),
    ('20/40/80Mhz XXXX','20/40/80mhz xxxx'),
    ('-','-'),
  )

  channelWidth = models.CharField(
    max_length = 100,
		choices = widthList,
		default = '-',
    )


  signal = models.CharField(max_length = 10)
  sn = models.CharField(max_length = 100)
  os = models.CharField(max_length = 100)
  type = models.CharField(max_length = 100)
  watt = models.FloatField(default=0)

  statusList = (
    ('Active','active'),
    ('Idle','idle'),
  )

  status = models.CharField(
    max_length = 7,
		choices = statusList,
		default = 'idle',
    )

  remark = models.TextField(blank=True, null=True)

  updated	= models.DateTimeField(auto_now=True)

  def __str__(self):
      return f'{self.id}. {self.deviceId}'