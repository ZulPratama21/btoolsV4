from django.urls import path

from . import views

app_name = 'databases'

urlpatterns = [
    path('client/', views.client, name='client'),
    path('odp/', views.odp, name='odp'),
    path('device/', views.device, name='device'),
]