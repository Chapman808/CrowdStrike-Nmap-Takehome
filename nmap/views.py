from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import NmapResult
import subprocess
import simplejson as json

def index(request):
    def _changesSinceLastScan(all_nmap_results):
        most_recent_scan = json.loads(all_nmap_results[0].ports)
        if all_nmap_results.count() >= 2:
            previous_scan = json.loads(all_nmap_results[1].ports)
        else: previous_scan = set()
        added = list(set(most_recent_scan) - set(previous_scan)) #added open ports since last scan
        removed = list(set(previous_scan) - set(most_recent_scan)) #closed ports since last scan
        return ["port opened: " + item for item in added] + ["port closed: " + item for item in removed] #return all added and removed ports with description

    host = request.session.get('host')  #current hostname to display results applied from submitNmap redirect
    all_nmap_results = NmapResult.objects.filter(host=host) 
    all_nmap_results = all_nmap_results.order_by('timestamp').reverse() #all results in reverse order by timestamp
    most_recent_scan = all_nmap_results[0]
    print(_changesSinceLastScan(all_nmap_results))
    return render(
        request, 
        'nmap.html', 
        {
            'all_results': all_nmap_results,
            'most_recent' : most_recent_scan,
            'open_port_changes' : _changesSinceLastScan(all_nmap_results)
        }
    )

def submitNmap(request):
    def validateHostname (host):
        if host: return host
        else: return ""

    def _getNmapResults (host):
        nmapProcess = subprocess.Popen(['nmap', host, '-p 0-1000', '--open', '-oG', '-'], stdout=subprocess.PIPE)
        grepPortsProcess = subprocess.Popen(['grep', 'Ports:'], stdin=nmapProcess.stdout, stdout=subprocess.PIPE)
        nmapProcess.stdout.close()
        return grepPortsProcess.stdout.read().decode('utf-8')

    def _formatNmapPorts (scanResult):
        if len(scanResult.split("\t")) > 1: scanResult = scanResult.split("\t")[1] #split off uneeded information
        scanResult = scanResult[len("Ports: ")::]  #strip off the 'Ports: ' indicator
        portsList = scanResult.split(", ") #split open ports into a list
        for port in portsList:
            port = port.split("/")[0]
        portsList = json.dumps(portsList)
        return portsList

    host = validateHostname(request.POST.get('host'))
    request.session['host'] = host  #set session variable for use by the index page in filtering results
    ports = _getNmapResults(host) #run the nmap command and return the string results
    portsList = _formatNmapPorts(ports) #filter the results and process them into a list

    dbObject = NmapResult(host=host, ports=portsList)
    dbObject.save()

    return HttpResponseRedirect('/')