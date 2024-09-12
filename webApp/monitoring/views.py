from django.shortcuts import render

# Create your views here.
def smokeping(request):
    return render(request, 'monitoring/smokeping.html')