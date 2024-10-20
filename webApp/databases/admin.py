from django.contrib import admin

# Register your models here.

from .models import UserDevice, Client, Odp, Device
from .forms import UserDeviceForm

class UserDeviceAdmin(admin.ModelAdmin):
    form = UserDeviceForm

class ClientAdmin(admin.ModelAdmin):
    search_fields = ['idpelanggan', 'necode','namapelanggan','ipremote']

class OdpAdmin(admin.ModelAdmin):
    search_fields = ['odpId', 'segmen']

class DeviceAdmin(admin.ModelAdmin):
    search_fields = ['pop', 'deviceId','remoteAddress','layer','routerFirewall','role','frequency','os','status']

admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Odp, OdpAdmin)
admin.site.register(Device, DeviceAdmin)