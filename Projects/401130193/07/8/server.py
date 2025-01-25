import socket

dns_data = {
    "example.org": "93.184.216.34",
    "yahoo.com": "98.137.246.8",
    "github.com": "140.82.121.4"
}

def fetch_ip(domain):
    """Resolves a domain to its corresponding IP address."""
    return dns_data.get(domain, "Domain not found")

def launch_dns_server():
    """Launches the DNS server to handle domain resolution requests."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12000))
    server_socket.listen(1)
    print("[SERVER] DNS server is up and running...")

    conn, addr = server_socket.accept()
    print(f"[SERVER] Connected to client: {addr}")

    while True:
        domain_request = conn.recv(1024).decode()
        if not domain_request or domain_request.lower() == 'close':
            print("[SERVER] Client disconnected.")
            break
        resolved_ip = fetch_ip(domain_request)
        conn.send(resolved_ip.encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    launch_dns_server()
