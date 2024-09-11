from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('device/', include('device')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),
]
