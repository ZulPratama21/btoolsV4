from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .scriptNetmation.generateScript import gConfC320OnuBridge, gConfC320OnuPppoe

@csrf_exempt
def apiConfC320OnuBridge(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sn = data.get('sn')
        ipAddress = data.get('ipAddress')
        limitasi = data.get('limitasi')
        neCode = data.get('neCode')
        subnetMask = data.get('subnetMask')
        modemType = data.get('modemType')

        result = gConfC320OnuBridge(sn,neCode,ipAddress,subnetMask,limitasi,modemType)

        response_data = {
            'status': 'success',
            'message': result
        }

        return JsonResponse(response_data)
    
@csrf_exempt
def apiConfC320OnuPppoe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sn = data.get('sn')
        limitasi = data.get('limitasi')
        neCode = data.get('neCode')
        modemType = data.get('modemType')

        result = gConfC320OnuPppoe(sn,neCode,ipAddress,subnetMask,limitasi,modemType)

        response_data = {
            'status': 'success',
            'message': result
        }

        return JsonResponse(response_data)

@login_required(redirect_field_name='next', login_url='/login')
def generateScript(request, generateApp):

    return render(request, f'configuration/{generateApp}.html')

