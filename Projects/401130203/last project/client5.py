import socket
def scan_ports(target_host, start_port, end_port):
    print(f"Scanning ports on {target_host} from {start_port} to {end_port}...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.5)
        try:
            client.connect((target_host, port))
            open_ports.append(port)
            print(f"Port {port} is open.")
        except (socket.timeout, ConnectionRefusedError):
            pass
