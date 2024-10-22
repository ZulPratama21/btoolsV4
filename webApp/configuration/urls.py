from django.urls import path
from . import views

app_name = 'configuration'

urlpatterns = [
    path('apiConfC320OnuBridge', views.apiConfC320OnuBridge, name='apiConfC320OnuBridge'),
    path('apiConfC320OnuPppoe', views.apiConfC320OnuPppoe, name='apiConfC320OnuPppoe'),
    path('apiConfC320OnuStatic', views.apiConfC320OnuStatic, name='apiConfC320OnuStatic'),
    path('apiConfC320OnuManyPacket', views.apiConfC320OnuManyPacket, name='apiConfC320OnuManyPacket'),
    path('generateScript/<str:generateApp>/', views.generateScript, name='generateScript'),
    path('confUserDevice', views.confUserDevice, name='confUserDevice'),
    path('sendConfDevice', views.sendConfDevice, name='sendConfDevice'),
    path('sendConfClient', views.sendConfClient, name='sendConfClient'),
]