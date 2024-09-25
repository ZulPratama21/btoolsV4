from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .scriptNetmation import troubleshootBhomeFtth, troubleshootDuFo

def getDataBhomeFtth(request):
    idLoc = request.GET.get('locationId')
    dataAll = troubleshootBhomeFtth.getAllData(idLoc)

    return JsonResponse(dataAll)

def getDataDuFo(request):
    idLoc = request.GET.get('locationId')
    dataAll = troubleshootDuFo.getAllData(idLoc)

    return JsonResponse(dataAll)

# Perlu dirapihkan kembali agar hanya 1 function cukup untuk menampung beberapa request menggunakan dynamic URL
@login_required(redirect_field_name='next', login_url='/login')
def bhomeFtth(request):
    return render(request, 'troubleshoot/bhomeFtth.html')

@login_required(redirect_field_name='next', login_url='/login')
def duFo(request):
    return render(request, 'troubleshoot/duFo.html')