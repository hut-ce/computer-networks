import socket

def dns_query_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 12356))
    print("Successfully connected to the DNS Server.")

    while True:
        domain_name = input("Please enter the domain name to resolve (type 'exit' to close): ").strip()
        if domain_name.lower() == 'exit':
            sock.send(b'exit')
            print("Exiting the DNS client.")
            break
        sock.send(domain_name.encode())
        ip_address = sock.recv(1024).decode()
        print(f"Resolved IP Address: {ip_address}")

    sock.close()

if __name__ == "__main__":
    dns_query_client()
