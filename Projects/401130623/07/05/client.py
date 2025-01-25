import socket

def scan_ports(server_ip, port_range):
    open_ports = []
    for port in port_range:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)  
        result = client_socket.connect_ex((server_ip, port))
        if result == 0:
            print(f"the port {port} is open\n")
            open_ports.append(port)
        else:
            print(f"the port {port} is closed\n")
        client_socket.close()
    print("list:")
    print(open_ports)

def scan():
    server_ip = '127.0.0.1'  
    port_range = range(1, 550)  
    scan_ports(server_ip, port_range)

if __name__ == "__main__":
    scan()
