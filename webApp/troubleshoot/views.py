from django.shortcuts import render

# Create your views here.
from .scriptNetmation import troubleshootBhomeFtth
from django.http import JsonResponse


def get_traffic_data(request):
    dataRouter = troubleshootBhomeFtth.getDataRouter('ca0019001')

    return JsonResponse(dataRouter)

def bhomeFtth(request):
    return render(request, 'troubleshoot/bhomeFtth.html')