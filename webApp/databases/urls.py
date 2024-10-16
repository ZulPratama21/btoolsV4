from django.urls import path

from . import views

app_name = 'databases'

urlpatterns = [
    path('odp/', views.odp, name='odp'),
]