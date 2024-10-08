from django.urls import path
from . import views

app_name = 'troubleshoot'

urlpatterns = [
    path('getDataBhomeFtth/', views.getDataBhomeFtth, name='getDataBhomeFtth'),
    path('getDataDuFo/', views.getDataDuFo, name='getDataDuFo'),
    path('bhomeFtth/', views.bhomeFtth, name='bhomeFtth'),
    path('bhomeFtth/configWifi/<str:deviceId>', views.configWifi, name='configWifi'),
    path('duFo/', views.duFo, name='duFo'),
]