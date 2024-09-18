from django.urls import path
from . import views

app_name = 'troubleshoot'

urlpatterns = [
    path('getData/', views.get_traffic_data, name='getData'),
    path('bhomeFtth/', views.bhomeFtth, name='bhomeFtth')
]