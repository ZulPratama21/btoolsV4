from django.urls import path
from . import views

app_name = 'troubleshoot'

urlpatterns = [
    path('traffic-data/', views.get_traffic_data, name='traffic-data'),
    path('bhomeFtth/', views.bhomeFtth, name='bhomeFtth')
]