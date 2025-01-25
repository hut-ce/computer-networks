import socket


def scan_ports(ip, port_range):

    op_port = []
    
    for port in port_range:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)  
        
        result = client_socket.connect_ex((ip, port))
        
        if result == 0:

            print(f"Port {port} is OPEN")
            op_port.append(port)
        else:
            
            print(f"Port {port} is CLOSED")
        
        client_socket.close()
    
    print("\nOpen Ports:")
    print(op_port)


def start_scan():
    ip = '127.0.0.1'  
    port_range = range(8000, 10100)  
    
    scan_ports(ip, port_range)

if __name__ == "__main__":
    start_scan()
