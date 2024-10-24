from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

from .models import Odp, Client, Device
from .command import update_odp_data

@login_required(redirect_field_name='next', login_url='/login')
def odp(request):
    query = request.GET.get('q')
    odps = Odp.objects.all().values()

    if query:
        odps = odps.filter(
            Q(odpId__icontains=query) |
            Q(tanggalinstalasi__icontains=query) |
            Q(portFilled__icontains=query) |
            Q(portRemaining__icontains=query) |
            Q(total_port__icontains=query) |
            Q(portOlt__icontains=query) |
            Q(oltIp__icontains=query) |
            Q(identityOlt__icontains=query) |
            Q(segmen__icontains=query) |
            Q(tikor__icontains=query) |
            Q(alamat__icontains=query) |
            Q(statusOpname__icontains=query) |
            Q(remark__icontains=query) |
            Q(updated__icontains=query)
        )

    paginator = Paginator(odps, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }

    if request.method == 'POST':
        update_odp_data()

        messages.success(request, "Data Ter-Update!!!")

        return redirect('databases:odp')

    return render(request, 'databases/odp.html',  context)

@login_required(redirect_field_name='next', login_url='/login')
def client(request):
    query = request.GET.get('q')
    clients = Client.objects.all().values()

    if query:
        clients = clients.filter(
            Q(idpelanggan__icontains=query) |
            Q(necode__icontains=query) |
            Q(namapelanggan__icontains=query) |
            Q(tanggalinstalasi__icontains=query) |
            Q(ipremote__icontains=query) |
            Q(deviceOs__icontains=query) |
            Q(portwinbox__icontains=query) |
            Q(portssh__icontains=query) |
            Q(portapi__icontains=query) |
            Q(portweb__icontains=query) |
            Q(iplinkmain__icontains=query) |
            Q(iplinkbackup__icontains=query) |
            Q(iptambahan__icontains=query) |
            Q(parentrouter__icontains=query) |
            Q(jenispaket__icontains=query) |
            Q(bwupload__icontains=query) |
            Q(bwdownload__icontains=query) |
            Q(aktivasibtools__icontains=query) |
            Q(connectto__icontains=query) |
            Q(onuid__icontains=query) |
            Q(portconnect__icontains=query) |
            Q(pop__icontains=query) |
            Q(mrtg__icontains=query) |
            Q(nagios__icontains=query) |
            Q(smokeping__icontains=query) |
            Q(media__icontains=query) |
            Q(redamansignalawal__icontains=query) |
            Q(remark__icontains=query)
        )
        
    paginator = Paginator(clients, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }

    return render(request, 'databases/client.html', context)

@login_required(redirect_field_name='next', login_url='/login')
def device(request):
    query = request.GET.get('q')
    devices = Device.objects.all().values()

    if query:
        devices = devices.filter(
            Q(pop__icontains=query) |
            Q(deviceId__icontains=query) |
            Q(installedDate__icontains=query) |
            Q(remoteAddress__icontains=query) |
            Q(addtionalIp__icontains=query) |
            Q(portWinbox__icontains=query) |
            Q(portSsh__icontains=query) |
            Q(portApi__icontains=query) |
            Q(portWeb__icontains=query) |
            Q(layer__icontains=query) |
            Q(routerFirewall__icontains=query) |
            Q(role__icontains=query) |
            Q(frequency__icontains=query) |
            Q(channelBand__icontains=query) |
            Q(channelWidth__icontains=query) |
            Q(signal__icontains=query) |
            Q(sn__icontains=query) |
            Q(os__icontains=query) |
            Q(type__icontains=query) |
            Q(watt__icontains=query) |
            Q(status__icontains=query) |
            Q(remark__icontains=query) |
            Q(updated__icontains=query)
        )
        
    paginator = Paginator(devices, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }

    return render(request, 'databases/device.html', context)