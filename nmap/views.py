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
    def _formatNmapPorts (scanResult):
        if len(scanResult.split("\t")) > 1: scanResult = scanResult.split("\t")[1] #split off uneeded information
        scanResult = scanResult[len("Ports: ")::]  #strip off the 'Ports: ' indicator
        portsList = scanResult.split(", ")
        print(portsList)
        return portsList

    host = validateHostname(request.POST.get('host'))

    nmapProcess = subprocess.Popen(['nmap', host, '-p 0-1000', '--open', '-oG', '-'], stdout=subprocess.PIPE)
    grepPortsProcess = subprocess.Popen(['grep', 'Ports:'], stdin=nmapProcess.stdout, stdout=subprocess.PIPE)
    nmapProcess.stdout.close()
    ports = grepPortsProcess.stdout.read().decode('utf-8')
    
    portsList = _formatNmapPorts(ports)
    dbObject = NmapResult(host=host, content=str(portsList))
    dbObject.save()

    return HttpResponseRedirect('/')