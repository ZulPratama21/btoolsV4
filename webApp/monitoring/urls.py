from django.urls import path

from .views import MonitoringViews

app_name = 'monitoring'

urlpatterns = [
    path('<str:templateName>/', MonitoringViews.as_view(), name='monitoringViews'),
]