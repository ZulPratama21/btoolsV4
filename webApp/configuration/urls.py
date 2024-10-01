from django.urls import path
from . import views

app_name = 'configuration'

urlpatterns = [
    path('apiConfC320OnuBridge', views.apiConfC320OnuBridge, name='apiConfC320OnuBridge'),
    path('apiConfC320OnuPppoe', views.apiConfC320OnuPppoe, name='apiConfC320OnuPppoe'),
    path('generateScript/<str:generateApp>/', views.generateScript, name='generateScript'),
]