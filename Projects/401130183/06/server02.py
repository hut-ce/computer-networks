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

def send_private_message(sender_socket, recipient_name, message):
    recipient_socket = None
    for client, username in clients.items():
        if username == recipient_name:
            recipient_socket = client
            break
    
    if recipient_socket:
        try:
            recipient_socket.send(f"Private message from {clients[sender_socket]}: {message}".encode('utf-8'))
            sender_socket.send(f"Message sent to {recipient_name}: {message}".encode('utf-8'))
        except:
            sender_socket.send(f"Failed to send message to {recipient_name}. They may have disconnected.".encode('utf-8'))
    else:
        sender_socket.send(f"User {recipient_name} not found.".encode('utf-8'))

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f"{username} connected.")
        broadcast(f"{username} joined the chat!")

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if message.startswith('@'):
                parts = message[1:].split(' ', 1)
                if len(parts) >= 2:
                    recipient_name = parts[0]
                    private_message = parts[1]
                    send_private_message(client_socket, recipient_name, private_message)
                else:
                    client_socket.send("Invalid private message format. Use @username message.".encode('utf-8'))
            elif message.lower() == 'exit':
                broadcast(f"{clients[client_socket]} has left the chat.", client_socket)
                print(f"{clients[client_socket]} disconnected.")
                break
            else:
                broadcast(f"{clients[client_socket]}: {message}", client_socket)
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
