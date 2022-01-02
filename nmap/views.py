from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import NmapResult
import subprocess

def index(request):
    all_nmap_results = NmapResult.objects.all()
    return render(
        request, 
        'nmap.html', 
        {'all_results': all_nmap_results}
    )

def submitNmap(request):
    def validateHostname (host):
        if host: return host
        else: return ""
    host = validateHostname(request.POST.get('host'))
    scanResult = subprocess.run(['nmap', host,'-p 0-1000'], stdout=subprocess.PIPE)
    dbObject = NmapResult(host=host, content=scanResult.stdout.decode('utf-8'))
    dbObject.save()
    return HttpResponseRedirect('/')