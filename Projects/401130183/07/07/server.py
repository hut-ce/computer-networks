import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 12345
SERVER_CERT = 'server.crt'
SERVER_KEY = 'server.key'

clients = []

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    client_socket.send(b'Welcome to the secure chat room!')

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Message received: {message.decode()}")
                broadcast(message, client_socket)
            else:
                client_socket.close()
                clients.remove(client_socket)
                break
        except:
            client_socket.close()
            clients.remove(client_socket)
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    
    server_socket = ssl.wrap_socket(server_socket, keyfile=SERVER_KEY, certfile=SERVER_CERT, server_side=True)
    print("Server is running and waiting for secure connections...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

start_server()
