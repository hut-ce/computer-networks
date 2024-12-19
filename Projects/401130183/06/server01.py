import socket
import threading

host = '0.0.0.0'
port = 12345
clients = {} 

def broadcast(message, sender_socket=None):
    for client, username in clients.items():
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                del clients[client]

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f"{username} connected.")
        broadcast(f"{username} joined the chat!")

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == 'exit':
                broadcast(f"{username} has left the chat.", client_socket)
                print(f"{username} disconnected.")
                break
            broadcast(f"{username}: {message}", client_socket)
    except:
        pass
    finally:
        client_socket.close()
        if client_socket in clients:
            del clients[client_socket]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print(f"Server started on {host}:{port}")

while True:
    client_socket, client_address = server.accept()
    print(f"New connection from {client_address}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()