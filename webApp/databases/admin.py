from django.contrib import admin

# Register your models here.

from .models import UserDevice
from .forms import UserDeviceForm

class UserDeviceAdmin(admin.ModelAdmin):
    form = UserDeviceForm

admin.site.register(UserDevice, UserDeviceAdmin)