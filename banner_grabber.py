def banner_grabber(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(b'HEAD / HTTP/1.1\r\n\r\n')
            banner = s.recv(1024)
            print(f"Banner: {banner.decode().strip()}")
    except Exception as e:
        print(f"Error: {e}")
