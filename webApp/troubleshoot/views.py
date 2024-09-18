from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .scriptNetmation import troubleshootBhomeFtth

@csrf_exempt  # Pastikan CSRF token diurus jika tidak digunakan di AJAX
def getData(request):
    idLoc = request.GET.get('locationId')
    hostList = ['103.73.72.182', '103.73.72.162', '103.73.72.222']
    dataRouter = None

    for host in hostList:
        try:
            dataRouter = troubleshootBhomeFtth.getDataRouter(idLoc, host, 'jul', 'Juliandi123!@#', '8728')

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
    else:
        return JsonResponse(dataRouter)

@login_required(redirect_field_name='next', login_url='/login')
def bhomeFtth(request):
    return render(request, 'troubleshoot/bhomeFtth.html')