from django.urls import path
from . import views

app_name = 'configuration'

urlpatterns = [
    path('confC320OnuBridge', views.confC320OnuBridge, name='confC320OnuBridge'),
    path('generateScript/<str:generateApp>/', views.generateScript, name='generateScript'),
]