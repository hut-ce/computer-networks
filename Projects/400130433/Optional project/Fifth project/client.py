import socket


def scan_ports(server_ip, port_range):
    open_ports = []
    
    for port in port_range:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)  
        
        result = client_socket.connect_ex((server_ip, port))
        
        if result == 0:
            print(f"Port {port} is OPEN")
            open_ports.append(port)
        else:
            print(f"Port {port} is CLOSED")
        
        client_socket.close()
    
    print("\nOpen Ports:")
    print(open_ports)


def start_scan():
    server_ip = '127.0.0.1'  
    port_range = range(8000, 10100)  
    
    scan_ports(server_ip, port_range)

if __name__ == "__main__":
    start_scan()
