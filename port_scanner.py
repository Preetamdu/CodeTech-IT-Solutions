import socket
from threading import Thread

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                print(f"Port {port} is open")
    except:
        pass

def port_scanner(host, ports):
    print(f"Scanning {host}...")
    for port in ports:
        Thread(target=scan_port, args=(host, port)).start()
