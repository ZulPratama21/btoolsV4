from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class MonitoringViews(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    redirect_field_name = 'next'

    def get_template_names(self):
        templateName = self.kwargs.get('templateName', None)
        
        return [f'monitoring/{templateName}.html']