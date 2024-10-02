from django.shortcuts import render, redirect

# Create your views here.
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .scriptNetmation import troubleshootBhomeFtth, troubleshootDuFo
from common.genieacsApi import zte1

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

@login_required(redirect_field_name='next', login_url='/login')
def configWifi(request, clientIp):
    locationId = request.GET.get('locationId')
    onuType = request.GET.get('onuType')

    if request.method == 'POST':
        ssid5 = request.POST.get('ssid5')
        ssid2 = request.POST.get('ssid2')
        passWifi5 = request.POST.get('passWifi5')
        passWifi2 = request.POST.get('passWifi2')

        if onuType.split('V')[0] == 'F670L':
            result5 = zte1.setWifi(clientIp, '5.8', ssid5, passWifi5)
            result2 = zte1.setWifi(clientIp, '2.4', ssid2, passWifi2)

        messages.success(request, f"<strong>{locationId.upper()}</strong><br><br>{result5['responseBody']}<br>{result2['responseBody']}<br>Konfirmasi perubahan dengan memasukan kembali ID ke kolom search dibawah!!")

        return redirect('troubleshoot:bhomeFtth')
    
    ssid5 = request.GET.get('ssid5')
    ssid2 = request.GET.get('ssid2')
    passWifi5 = request.GET.get('passWifi5')
    passWifi2 = request.GET.get('passWifi2')

    context = {
        'clientIp':clientIp,
        'ssid5':ssid5,
        'ssid2':ssid2,
        'passWifi5':passWifi5,
        'passWifi2':passWifi2,
    }



    return render(request, 'troubleshoot/configWifi.html', context)
