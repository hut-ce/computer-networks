import socket
import ssl
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def handle_client_connection(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"Received: {message}")
        client_socket.sendall(f"Echo: {message}".encode('utf-8'))
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print("Server is Running and is waiting for connections...")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr[1]} is connected to the server!")
        secure_client_socket = context.wrap_socket(client_socket, server_side=True)
        client_handler = threading.Thread(target=handle_client_connection, args=(secure_client_socket,))
        client_handler.start()


if __name__ == '__main__':
    main()
