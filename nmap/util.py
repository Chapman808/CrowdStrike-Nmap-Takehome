import socket
import subprocess
from django.http.response import JsonResponse
import simplejson as json
from django.core import serializers
def validateHostname (host):
    if not host: raise ValueError("Please enter a hostname.")
    try:
        host = socket.gethostbyname(host)
    except (socket.gaierror): raise ValueError("Invalid hostname.")
    return host

def getNmapResults (host):
    nmapProcess = subprocess.Popen(['nmap', host, '-p 0-1000', '--open', '-oG', '-'], stdout=subprocess.PIPE)
    grepPortsProcess = subprocess.Popen(['grep', 'Ports:'], stdin=nmapProcess.stdout, stdout=subprocess.PIPE)
    nmapProcess.stdout.close()
    return grepPortsProcess.stdout.read().decode('utf-8')

def formatNmapPorts (scanResult):
    if len(scanResult.split("\t")) > 1: scanResult = scanResult.split("\t")[1] #split off uneeded information
    scanResult = scanResult[len("Ports: ")::]  #strip off the 'Ports: ' indicator
    portsList = scanResult.split(", ") #split open ports into a list
    for port in portsList:
        port = port.split("/")[0]
    portsList = json.dumps(portsList)
    return portsList

def formatNmapResultsAsJson(nmapResultQuerySet):
    jsonResults = ""
    return jsonResults