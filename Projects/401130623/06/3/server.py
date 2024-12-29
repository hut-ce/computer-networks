import socket
import threading

clients = []
client_names = {}

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                client.close()
                clients.remove(client)

def private_message(message, recipient_name):
    for client, name in client_names.items():
        if name == recipient_name:
            try:
                client.send(message)
                return True
            except Exception as e:
                print(f"Error sending private message: {e}")
                client.close()
                clients.remove(client)
                return False
    return False

def handle_client(client_socket, addr):
    name = client_socket.recv(1024).decode('utf-8')
    client_names[client_socket] = name
    welcome_message = f"{name} has joined the chat!"
    print(welcome_message)
    broadcast(welcome_message.encode('utf-8'), client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            
            message_decoded = message.decode('utf-8')
            if message_decoded.startswith("@"):
                recipient_name, private_msg = message_decoded[1:].split(" ", 1)
                private_message(f"Private from {name}: {private_msg}".encode('utf-8'), recipient_name)
            else:
                broadcast(f"{name}: {message_decoded}".encode('utf-8'), client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    clients.remove(client_socket)
    farewell_message = f"{name} has left the chat."
    print(farewell_message)
    broadcast(farewell_message.encode('utf-8'), client_socket)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 10000))
server.listen(5)
print("Server is listening on port 10000")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    print(f"Accepted connection from {addr}")
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
