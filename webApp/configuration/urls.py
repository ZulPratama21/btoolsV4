from django.urls import path
from . import views

app_name = 'configuration'

urlpatterns = [
    path('generateScript/<str:generateApp>/', views.generateScript, name='generateScript'),
]