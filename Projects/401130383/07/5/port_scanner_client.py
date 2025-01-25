import socket


def scan_portes(target: str, start_port: int, end_port: int):
    open_portes = []
    print(f'Scanning {target} from port {start_port} to {end_port}...')

    for port in range(start_port, end_port + 1):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(0.5)
        result = client_socket.connect_ex((target, port))
        if result == 0:
            print(f'Port {port} is open')
            open_portes.append(port)
        client_socket.close()
    
    return open_portes


if __name__ == '__main__':
    scan_portes('127.0.0.1', 8000, 8050)
