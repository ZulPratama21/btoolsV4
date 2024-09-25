from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .scriptNetmation.generateScript import gConfC320OnuBridge

@csrf_exempt
def confC320OnuBridge(request):
    if request.method == 'POST':
        # Mendapatkan data dari request body
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
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def generateScript(request, generateApp):

    return render(request, f'configuration/{generateApp}.html')

