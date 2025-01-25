import socket


def port_scanner(host: str, range_start: int, range_end: int):
    """Scan ports on the target host to find open ports."""
    print(f'[SCAN START] Scanning {host} from port {range_start} to {range_end}...')
    found_ports = []

    for port in range(range_start, range_end + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
                scanner.settimeout(0.3)  # Reduced timeout for quicker scanning
                if scanner.connect_ex((host, port)) == 0:
                    print(f'[OPEN] Port {port} is open.')
                    found_ports.append(port)
        except Exception as e:
            print(f'[ERROR] Unable to scan port {port}: {e}')

    print(f'[SCAN COMPLETE] Open ports: {found_ports}')


if __name__ == '__main__':
    target_host = '127.0.0.1'
    port_scanner(target_host, 8000, 8050)
