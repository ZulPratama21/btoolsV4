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
from databases.models import UserDevice, Device
from common.utils import decryptor, confRouterOs

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
                }
            )

        configList = []
        for user in userList:
            if action == 'add':
                configList.append(f"/user add name={user['user']} password={user['password']} group={user['group']}")

            if action == 'edit':
                configList.append(f"/user set {user['user']} name={user['user']} password={user['password']} group={user['group']}")

            else:
                configList.append(f"/user remove {user['user']}")

        userLogin = UserDevice.objects.get(user='bnettools')

        for device in deviceList:
            output = confRouterOs(
                device['remoteAddress'],
                userLogin.user,
                decryptor(userLogin.password),
                device['port'],
                'Konfigurasi User',
                configList,
                'n')

        return HttpResponse(json.dumps(output, indent=4))
    
    users = UserDevice.objects.all().values()
    devices = Device.objects.all().values()

    context = {
        'users': users,
        'devices': devices,
    }

    return render(request, f'configuration/confUserDevice.html', context)