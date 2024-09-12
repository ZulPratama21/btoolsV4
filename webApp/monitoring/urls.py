from django.urls import path

from . import views

app_name = 'monitoring'

urlpatterns = [
    path('smokeping/', views.smokeping, name='smokeping'),
]