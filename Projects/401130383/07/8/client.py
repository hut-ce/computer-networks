import socket

def dns_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12356))
    print("Connected to DNS Server.")

    while True:
        domain = input("Enter domain to resolve (or type 'exit' to quit): ").strip()
        if domain.lower() == 'exit':
            client_socket.send(b'exit')
            break
        client_socket.send(domain.encode())
        response = client_socket.recv(1024).decode()
        print(f"IP Address: {response}")

    client_socket.close()

if __name__ == "__main__":
    dns_client()
