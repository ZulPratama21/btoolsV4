from django.shortcuts import render

# Create your views here.

from .models import Odp

def odp(request):
    Odps = Odp.objects.all().values()
    
    context = {
        'Odps':Odps
    }

    return render(request, 'databases/odp.html',  context)