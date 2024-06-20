# server
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
MAX_CLIENTS = 5

clients = []

def handle_client(client_socket, client_address):
    print(f"Client connected: {client_address}")
    client_name = client_socket.recv(1024).decode('utf-8')
    print(f"Client name: {client_name}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"{client_name}: {message}")

        # Broadcast message to all clients
        for c in clients:
            if c != client_socket:
                c.sendall(f"{client_name}: {message}".encode('utf-8'))

    client_socket.close()
    clients.remove(client_socket)
    print(f"Client disconnected: {client_address}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server is running...")

    while True:
        client_socket, client_address = server_socket.accept()
        if len(clients) < MAX_CLIENTS:
            clients.append(client_socket)
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
        else:
            print("Maximum number of clients reached. Connection rejected.")

if name == "main":
    main()