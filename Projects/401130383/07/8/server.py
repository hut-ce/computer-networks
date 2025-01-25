import socket

dns_records = {
    "example.com": "93.184.216.34",
    "google.com": "142.250.190.78",
    "openai.com": "104.20.22.46"
}

def handle_dns_query(domain):
    return dns_records.get(domain, "Domain not found.")

def dns_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12356))
    server_socket.listen(1)
    print("DNS Server is listening...")

    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    while True:
        domain = conn.recv(1024).decode()
        if not domain or domain.lower() == 'exit':
            print("Client disconnected.")
            break
        response = handle_dns_query(domain)
        conn.send(response.encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    dns_server()
