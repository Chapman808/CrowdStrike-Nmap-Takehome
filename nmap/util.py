import socket
import subprocess
import simplejson as json

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
    portsList = [port.split("/")[0] for port in portsList]
    portsList = json.dumps(portsList)
    portsList = '[]' if portsList == '[""]' else portsList
    return portsList

def changesSinceLastScan(all_nmap_results):
    most_recent_scan = json.loads(all_nmap_results[0].ports) if all_nmap_results else set()
    if all_nmap_results.count() >= 2:
        previous_scan = json.loads(all_nmap_results[1].ports)
    else: previous_scan = set()
    added = list(set(most_recent_scan) - set(previous_scan)) #added open ports since last scan
    removed = list(set(previous_scan) - set(most_recent_scan)) #closed ports since last scan
    return ["port opened: " + item for item in added] + ["port closed: " + item for item in removed] #return all added and removed ports with description