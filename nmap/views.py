import re
from django.db.models.expressions import Value
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import NmapResult
from .util import formatNmapResultsAsJson, validateHostname, getNmapResults, formatNmapPorts, formatNmapResultsAsJson
import simplejson as json
from django.core import serializers

def index(request):
    def _changesSinceLastScan(all_nmap_results):
        most_recent_scan = json.loads(all_nmap_results[0].ports) if all_nmap_results else set()
        if all_nmap_results.count() >= 2:
            previous_scan = json.loads(all_nmap_results[1].ports)
        else: previous_scan = set()
        added = list(set(most_recent_scan) - set(previous_scan)) #added open ports since last scan
        removed = list(set(previous_scan) - set(most_recent_scan)) #closed ports since last scan
        return ["port opened: " + item for item in added] + ["port closed: " + item for item in removed] #return all added and removed ports with description

    host = request.session.get('host')  #current hostname to display results applied from submitNmap redirect
    error = request.session.get('error') if request.session.get('error') else '' #get any error messages passed through session
    request.session['error'] = '' #reset error value

    all_nmap_results = NmapResult.objects.filter(host=host) 
    all_nmap_results = all_nmap_results.order_by('timestamp').reverse() #all results in reverse order by timestamp
    most_recent_scan = all_nmap_results[0] if all_nmap_results else None
    print(_changesSinceLastScan(all_nmap_results))
    return render(
        request, 
        'nmap.html', 
        {
            'all_results': all_nmap_results,
            'most_recent' : most_recent_scan,
            'open_port_changes' : _changesSinceLastScan(all_nmap_results),
            'error' : error
        }
    )

def submitNmap(request):
    try:
        host = validateHostname(request.POST.get('host'))
    except ValueError as err:
        request.session['host'] = ''
        request.session['error'] = str(err) #set session variable for use by the index page in filtering results
        return HttpResponseRedirect('/') 

    request.session['host'] = host  #set session variable for use by the index page in filtering results
    ports = getNmapResults(host) #run the nmap command and return the string results
    portsList = formatNmapPorts(ports) #filter the results and process them into a list

    #create and save new Nmap result to DB Model
    dbObject = NmapResult(host=host, ports=portsList)
    dbObject.save()

    return HttpResponseRedirect('/')

def getHostScansAsJson(request):
    try:
        host = validateHostname(request.GET.get('host'))
    except ValueError as err:
        return HttpResponse(content=str(err), status=400)
    results = NmapResult.objects.filter(host=host).all()
    jsonResults = serializers.serialize("json", results)
    return HttpResponse(jsonResults)