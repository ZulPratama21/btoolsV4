from django.urls import path
from . import views

app_name = 'troubleshoot'

urlpatterns = [
    path('getData/', views.getData, name='getData'),
    path('bhomeFtth/', views.bhomeFtth, name='bhomeFtth')
]