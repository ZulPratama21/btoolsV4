from django.shortcuts import render

# Create your views here.

def confC320OnuBridge(request):
    pass

def generateScript(request, generateApp):

    return render(request, f'configuration/{generateApp}.html')

