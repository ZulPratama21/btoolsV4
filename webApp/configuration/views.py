from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .scriptNetmation.generateScript import (
    gConfC320OnuBridge,
    gConfC320OnuPppoe,
    gConfC320OnuStatic,
    gConfC320OnuManyPacket
    )

from .scriptNetmation.activation import deviceActivation
from databases.models import UserDevice, Device, Client
from common.utils import decryptor, confRouterOs
from databases.forms import deviceForm

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
        
        result = gConfC320OnuPppoe(sn,neCode,limitasi,modemType)

        response_data = {
            'status': 'success',
            'message': result
        }

        return JsonResponse(response_data)
    
@csrf_exempt
def apiConfC320OnuStatic(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sn = data.get('sn')
        ipAddress = data.get('ipAddress')
        limitasi = data.get('limitasi')
        neCode = data.get('neCode')
        subnetMask = data.get('subnetMask')
        modemType = data.get('modemType')
        
        result = gConfC320OnuStatic(sn,neCode,ipAddress,subnetMask,limitasi,modemType)

        response_data = {
            'status': 'success',
            'message': result
        }

        return JsonResponse(response_data)

@csrf_exempt
def apiConfC320OnuManyPacket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vlanGw = data.get('vlanGw')
        sn = data.get('sn')
        ipAddress = data.get('ipAddress')
        limitasi = data.get('limitasi')
        neCodes = data.get('neCodes')
        modemType = data.get('modemType')

        result = gConfC320OnuManyPacket(vlanGw, sn,neCodes,ipAddress,limitasi,modemType)

        response_data = {
            'status': 'success',
            'message': result
        }
        
        return JsonResponse(response_data)

@login_required(redirect_field_name='next', login_url='/login')
def generateScript(request, generateApp):

    return render(request, f'configuration/{generateApp}.html')

@login_required(redirect_field_name='next', login_url='/login')
def confUserDevice(request):
    if request.method == 'POST':
        selected_users = request.POST.getlist('selectedUsers')
        selected_devices = request.POST.getlist('selectedDevices')
        users = UserDevice.objects.filter(id__in=selected_users)
        devices = Device.objects.filter(id__in=selected_devices)
        action = request.POST.get('action')
        
        userList = []
        for user in users:
            plainPass = decryptor(user.password)
            group = user.group.lower()
            userList.append(
                {
                    'user': user.user,
                    'password': plainPass,
                    'group': group,
                }
            )

        deviceList = []
        for device in devices:
            deviceList.append(
                {
                    'remoteAddress': device.remoteAddress,
                    'port': device.portSsh,
                    'os': device.os,
                }
            )

        configList = []
        for user in userList:
            if action == 'add':
                configList.append(f"/user add name={user['user']} password={user['password']} group={user['group']}")

            elif action == 'edit':
                configList.append(f"/user set {user['user']} name={user['user']} password={user['password']} group={user['group']}")

            else:
                configList.append(f"/user remove {user['user']}")

        userLogin = UserDevice.objects.get(user='bnettools')

        outputList = []
        for device in deviceList:
            if device['os'].lower() == 'routeros':
                output = confRouterOs(
                    device['remoteAddress'],
                    userLogin.user,
                    decryptor(userLogin.password),
                    device['port'],
                    'Konfigurasi User',
                    configList,
                    'n')

            else:
                output = f"{device['remoteAddress']} || {device['os']} || Btools belum support OS tersebut"
            
            outputList.append(output)
        
        context = {
            'output':outputList,
            'source':'configuration:confUserDevice',
        }

        return render(request, f'logOutput.html', context)
    
    users = UserDevice.objects.all().values()
    devices = Device.objects.all().values()

    context = {
        'users': users,
        'devices': devices,
    }

    return render(request, f'configuration/confUserDevice.html', context)

@login_required(redirect_field_name='next', login_url='/login')
def sendConfDevice(request):
    if request.method == 'POST':
        configInput = request.POST.get('config')
        configList = configInput.split('\r\n')

        selected_devices = request.POST.getlist('selectedDevices')
        devices = Device.objects.filter(id__in=selected_devices)
        
        deviceList = []
        for device in devices:
            deviceList.append(
                {
                    'remoteAddress': device.remoteAddress,
                    'port': device.portSsh,
                    'os': device.os,
                }
            )

        user = request.POST.get('user')
        password = request.POST.get('password')
        
        outputList = []
        for device in deviceList:
            if device['os'].lower() == 'routeros':
                output = confRouterOs(
                    device['remoteAddress'],
                    user,
                    password,
                    device['port'],
                    'Mengirim Konfigurasi Device',
                    configList,
                    'n')
                
            else:
                output = f"{device['remoteAddress']} || {device['os']} || Btools belum support OS tersebut"
        
            outputList += output
            
        context = {
            'output':outputList,
            'source':'configuration:sendConfDevice',
        }
        
        return render(request, f'logOutput.html', context)

    users = UserDevice.objects.all().values()
    devices = Device.objects.all().values()

    context = {
        'users': users,
        'devices': devices,
    }

    return render(request, f'configuration/sendConfDevice.html', context)

@login_required(redirect_field_name='next', login_url='/login')
def sendConfClient(request):
    if request.method == 'POST':
        configInput = request.POST.get('config')
        configList = configInput.split('\r\n')

        selected_devices = request.POST.getlist('selectedDevices')
        clients = Client.objects.filter(id__in=selected_devices)
        
        clientList = []
        for client in clients:
            clientList.append(
                {
                    'remoteAddress': client.ipremote,
                    'port': client.portssh,
                    'os': client.deviceOs,
                }
            )

        user = request.POST.get('user')
        password = request.POST.get('password')
        
        outputList = []
        for client in clientList:
            if client['os'].lower() == 'routeros':
                output = confRouterOs(
                    client['remoteAddress'],
                    user,
                    password,
                    client['port'],
                    'Mengirim Konfigurasi Client',
                    configList,
                    'n')
                
            else:
                output = f"{client['remoteAddress']} || {client['os']} || Btools belum support OS tersebut"
        
            outputList += output
            
        context = {
            'output':outputList,
            'source':'configuration:sendConfClient',
        }
        
        return render(request, f'logOutput.html', context)

    users = UserDevice.objects.all().values()
    clients = Client.objects.all().values()

    context = {
        'users': users,
        'clients': clients,
    }

    return render(request, f'configuration/sendConfClient.html', context)

@login_required(redirect_field_name='next', login_url='/login')
def activationDevice(request):
    if request.method == 'POST':
        form = deviceForm(request.POST)
        if form.is_valid():
            pop = form.cleaned_data['pop']
            deviceId = form.cleaned_data['deviceId']
            remoteAddress = form.cleaned_data['remoteAddress']
            portSsh = form.cleaned_data['portSsh']
            routerFirewall = form.cleaned_data['routerFirewall']
            os = form.cleaned_data['os']

            user = request.POST.get('user')
            password = request.POST.get('password')

            result = deviceActivation(remoteAddress, user, password, portSsh, deviceId, pop, routerFirewall)

            # Checking error
            for log in result:
                if 'Gagal' in log:
                    context = {
                        'output': result,
                        'source': 'configuration:activationDevice',
                    }
                    
                    return render(request, 'logOutput.html', context)
                
            context = {
                'output': result,
                'source': 'configuration:activationDevice',
            }

            form.save()
            return render(request, 'logOutput.html', context)        
    
    users = UserDevice.objects.all().values()
    form = deviceForm()

    context = {
        'form': form,
        'users': users,
    }

    return render(request, 'configuration/activationDevice.html', context)