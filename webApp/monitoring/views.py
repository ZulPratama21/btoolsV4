from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class MonitoringViews(TemplateView):

    def get_template_names(self):
        templateName = self.kwargs.get('templateName', None)
        
        return [f'monitoring/{templateName}.html']