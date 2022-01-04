from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import NmapResult
from .util import validateHostname, getNmapResults, formatNmapPorts, changesSinceLastScan
import simplejson as json
from django.core import serializers
from rest_framework.views import APIView
from .permissions import Check_API_KEY_Auth

def index(request):
    host = request.session.get('host')  #current hostname to display results applied from submitNmap redirect
    error = request.session.get('error') if request.session.get('error') else '' #get any error messages passed through session
    request.session['error'] = '' #reset error value

    all_nmap_results = NmapResult.objects.filter(host=host) 
    all_nmap_results = all_nmap_results.order_by('timestamp').reverse() #all results in reverse order by timestamp
    most_recent_scan = all_nmap_results[0] if all_nmap_results else None
    return render(
        request, 
        'nmap.html', 
        {
            'all_results': all_nmap_results,
            'most_recent' : most_recent_scan,
            'open_port_changes' : changesSinceLastScan(all_nmap_results),
            'error' : error
        }
    )

class SubmitNmap(APIView):
    permission_classes = [Check_API_KEY_Auth]
    def post(self, request):
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