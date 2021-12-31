from django.shortcuts import render
import subprocess

def index(request):
    host = request.GET.get('host')
    if host:
        results = subprocess.run(['nmap', host,'-p 0-1000'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    else: results = ""

    context = {'results': results}
    return render(request, 'nmap.html', context)