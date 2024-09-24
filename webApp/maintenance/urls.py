from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('checkBgpPeer/', views.checkBgpPeer, name='checkBgpPeer'),
]