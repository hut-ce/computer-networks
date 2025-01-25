import socket

def scan_ports(host, start_port, end_port):
    print(f"Scanning ports on {host} from {start_port} to {end_port}...")
    for port in range(start_port, end_port + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)  # Short timeout for faster scanning
            s.connect((host, port))
            print(f"Port {port} is open.")
            s.close()
        except:
            print(f"Port {port} is closed.")

def port_scan_client():
    host = input("Enter server hostname (default: localhost): ").strip() or 'localhost'
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    scan_ports(host, start_port, end_port)

if __name__ == "__main__":
    port_scan_client()
