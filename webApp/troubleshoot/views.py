from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .scriptNetmation import troubleshootBhomeFtth, troubleshootDuFo
from common.oidLib import dictOltIp

@csrf_exempt  # Pastikan CSRF token diurus jika tidak digunakan di AJAX
def getDataBhomeFtth(request):
    idLoc = request.GET.get('locationId')
    hostList = ['103.73.72.182', '103.73.72.162', '103.73.72.222'] #Perlu dirubah ke database
    dataRouter = None

    for host in hostList:
        try:
            dataRouter = troubleshootBhomeFtth.getDataRouter(idLoc, host, 'neteng', 'netEngineerBnet', '8728') #Akses user masih static, harus ambil dari database

        except Exception as e:
            continue

    if dataRouter is None:
        return JsonResponse({
            'statusClient': 'Null',
            'maxUpload': 'X',
            'maxDownload': 'X',
            'tUpload': 'X',
            'tDownload': 'X',
            'latency': 'X',
        })
    
    neCode = (dataRouter['neCode'])
    oltIp = dictOltIp[neCode[:-4]] # perlu dirubah ke database
    oltPort = neCode[-4:-2]
    onuPort = int(neCode[-2:])

    try:
        dataOlt = troubleshootBhomeFtth.getDataOlt(oltIp,'intbnet',oltPort,onuPort)

    except Exception as e:
        dataOlt = {
                'state': 'Error',
                'redaman' : 'X',
                'authpass': 'X',
                'offline': 'X',
                'type': 'X',
                'name': 'X',
                'serialNumber': 'X',
            }

    dataAll = {**dataRouter, **dataOlt}

    return JsonResponse(dataAll)

def getDataDuFo(request):
    idLoc = request.GET.get('locationId')
    hostList = ['103.73.72.72', '103.73.72.73', '103.73.72.74'] #Perlu dirubah ke database
    dataRouter = None

    for host in hostList:
        try:
            dataRouter = troubleshootDuFo.getDataRouter(idLoc, host, 'neteng', 'netEngineerBnet', '8728') #Akses user masih static, harus ambil dari database
            
        except Exception as e:
            continue

    if dataRouter is None:
        return JsonResponse({
            'statusClient': 'Null',
            'maxUpload': 'X',
            'maxDownload': 'X',
            'tUpload': 'X',
            'tDownload': 'X',
            'latency': 'X',
            'clientIp': 'X',
            'clientName': 'X',
        })

    return JsonResponse(dataRouter)

@login_required(redirect_field_name='next', login_url='/login')
def bhomeFtth(request):
    return render(request, 'troubleshoot/bhomeFtth.html')

@login_required(redirect_field_name='next', login_url='/login')
def duFo(request):
    return render(request, 'troubleshoot/duFo.html')