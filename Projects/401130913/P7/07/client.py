import socket
import ssl

def connect_securely():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    secure_client = context.wrap_socket(client, server_hostname="127.0.0.1")

    secure_client.connect(("127.0.0.1", 10000))
    print(secure_client.recv(1024).decode())
    secure_client.close()

if __name__ == "__main__":
    connect_securely()
