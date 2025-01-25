import socket

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def scan_ports(host, start_port, end_port):
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))  
        
        if result == 0:
            print(f"Port {port} is open")
            open_ports.append(port)
        else:
            print(f"Port {port} is closed")
        
        sock.close()
    
    return open_ports

if __name__ == "__main__":
    target_host = get_local_ip()  
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))
    
    print(f"Scanning ports on {target_host} from {start_port} to {end_port}...")
    open_ports = scan_ports(target_host, start_port, end_port)
    
    print("\nOpen ports:")
    for port in open_ports:
        print(port)
