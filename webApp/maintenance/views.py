from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .scriptNetmation.checkBgpPeer import getBgpList

@login_required(redirect_field_name='next', login_url='/login')
def checkBgpPeer(request):
    # Harus dirubah datanya menjadi ke database
    bgpDevices = [
        '103.73.72.3',
        '103.73.72.2',
        '103.73.72.42',
        '103.73.72.43',
        '103.73.72.1',
    ]

    context = {
        'bgpList':getBgpList(bgpDevices)
    }

    return render(request, "maintenance/checkBgpPeer.html", context)