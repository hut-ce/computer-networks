import socket


port = 55555


def scaning_ports(server_ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)
        result = client_socket.connect_ex((server_ip, port))
        if result == 0:
            open_ports.append(port)
        client_socket.close()
    return open_ports


ip = socket.gethostbyname(socket.gethostname())
start_port = 1
end_port = 1024

print(f"Scanning {ip} from port {start_port} to {end_port}...")
open_ports = scaning_ports(ip, start_port, end_port)

if open_ports:
    print("Open ports:")
    print("[")
    i = 0
    for port in (open_ports):
        print(f"{i}. {port}!")
        i += 1
    print("]")
else:
    print("No open ports!")
