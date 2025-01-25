import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def scan_ports(server_ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)
        result = client_socket.connect_ex((server_ip, port))
        if result == 0:
            open_ports.append(port)
        client_socket.close()
    return open_ports


def main():
    server_ip = IP
    start_port = 1
    end_port = 1024

    print(f"Scanning {server_ip} from port {start_port} to {end_port}...")
    open_ports = scan_ports(server_ip, start_port, end_port)

    if open_ports:
        print("Open ports:")
        
        for port in open_ports:
            print(port)

    else:
        print("No open ports found!")


if __name__ == '__main__':
    main()
