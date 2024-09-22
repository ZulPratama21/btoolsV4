from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .scriptNetmation import troubleshootBhomeFtth
from common.oidLib import dictOltIp

@csrf_exempt  # Pastikan CSRF token diurus jika tidak digunakan di AJAX
def getData(request):
    idLoc = request.GET.get('locationId')
    hostList = ['103.73.72.182', '103.73.72.162', '103.73.72.222']
    dataRouter = None

    for host in hostList:
        try:
            dataRouter = troubleshootBhomeFtth.getDataRouter(idLoc, host, 'neteng', 'netEngineerBnet', '8728')

        except Exception as e:
            error = 'null'
            continue

    if dataRouter is None:
        return JsonResponse({
            'statusClient': error,
            'maxUpload': 'X',
            'maxDownload': 'X',
            'tUpload': 'X',
            'tDownload': 'X',
            'latency': 'X',
        })
    
    neCode = (dataRouter['neCode'])
    oltIp = dictOltIp[neCode[:-4]]
    oltPort = neCode[-4:-2]
    onuPort = int(neCode[-2:])

    dataOlt = None

    dataOlt = troubleshootBhomeFtth.getDataOlt(oltIp,'intbnet',oltPort,onuPort)

    dataAll = {**dataRouter, **dataOlt}

    return JsonResponse(dataAll)

@login_required(redirect_field_name='next', login_url='/login')
def bhomeFtth(request):
    return render(request, 'troubleshoot/bhomeFtth.html')