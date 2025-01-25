import socket

def scan_ports(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1)
        try:
            client.connect((ip, port))
            open_ports.append(port)
        except:
            pass
        finally:
            client.close()
    return open_ports

if __name__ == "__main__":
    ip = '127.0.0.1' 
    start_port = 8000
    end_port = 8005
    open_ports = scan_ports(ip, start_port, end_port)
    print(f"Open ports: {open_ports}")
