import socket

dns_records = {
    "example.com": "93.184.216.34",
    "google.com": "142.250.190.78",
    "openai.com": "104.20.22.46"
}

def resolve_domain(domain_name):
    return dns_records.get(domain_name, "Domain not found.")

def start_dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 12356))
    sock.listen(1)
    print("DNS Server is running and waiting for connections...")

    connection, client_address = sock.accept()
    print(f"Connection established with {client_address}")

    while True:
        domain_name = connection.recv(1024).decode()
        if not domain_name or domain_name.lower() == 'exit':
            print("Client has disconnected.")
            break
        result = resolve_domain(domain_name)
        connection.send(result.encode())

    connection.close()
    sock.close()

if __name__ == "__main__":
    start_dns_server()
