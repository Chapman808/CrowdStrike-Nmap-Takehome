import socket

def validateHostname (host):
    if not host: raise ValueError("Please enter a hostname.")
    try:
        host = socket.gethostbyname(host)
    except (socket.gaierror): raise ValueError("Invalid hostname.")
    return host