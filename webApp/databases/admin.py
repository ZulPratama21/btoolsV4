from django.contrib import admin

# Register your models here.

from .models import UserDevice, Client, Odp
from .forms import UserDeviceForm

class UserDeviceAdmin(admin.ModelAdmin):
    form = UserDeviceForm

class ClientAdmin(admin.ModelAdmin):
    search_fields = ['idpelanggan', 'necode','namapelanggan','ipremote']

class OdpAdmin(admin.ModelAdmin):
    search_fields = ['odpId', 'segmen']

admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Odp, OdpAdmin)