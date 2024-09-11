from django.views.generic import TemplateView


class index(TemplateView):
    template_name = "index.html"

    def get_index(self, **kwargs):
        context = {}
        
        return context