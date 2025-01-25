import socket

def query_dns():
    """Queries the DNS server for domain resolution."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12000))
    print("[CLIENT] Connected to the DNS server.")

    while True:
        domain = input("[CLIENT] Enter a domain to resolve (or 'close' to exit): ").strip()
        if domain.lower() == 'close':
            client_socket.send(b'close')
            print("[CLIENT] Exiting DNS client...")
            break
        client_socket.send(domain.encode())
        ip_result = client_socket.recv(1024).decode()
        print(f"[CLIENT] Resolved IP: {ip_result}")

    client_socket.close()

if __name__ == "__main__":
    query_dns()
