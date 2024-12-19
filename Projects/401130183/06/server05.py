import socket
import threading

host = '0.0.0.0'
port = 12345
clients = {}  
blocked_users = {} 
roles = {}  

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

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
            encrypted_message = caesar_cipher(message, 2)
            recipient_socket.send(f"Private message from {clients[sender_socket]}: {encrypted_message}".encode('utf-8'))
            sender_socket.send(f"Message sent to {recipient_name}: {encrypted_message}".encode('utf-8'))
        except:
            sender_socket.send(f"Failed to send message to {recipient_name}. They may have disconnected.".encode('utf-8'))
    else:
        sender_socket.send(f"User {recipient_name} not found.".encode('utf-8'))

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        blocked_users[username] = [] 
        roles[username] = 'user'  
        print(f"{username} connected.")
        broadcast(f"{username} joined the chat!")

        if username == "admin":
            roles[username] = 'admin'
        elif username == "moderator":
            roles[username] = 'moderator'

        while True:
            message = client_socket.recv(1024).decode('utf-8')

            if message.startswith('!block'):
                blocked_user = message.split(' ')[1]
                if roles[clients[client_socket]] == 'admin' or roles[clients[client_socket]] == 'moderator':
                    if blocked_user not in blocked_users[username]:
                        blocked_users[username].append(blocked_user)
                        client_socket.send(f"You have blocked {blocked_user}.".encode('utf-8'))
                        print(f"{username} blocked {blocked_user}")
                    else:
                        client_socket.send(f"{blocked_user} is already blocked.".encode('utf-8'))
                else:
                    client_socket.send("You do not have permission to block users.".encode('utf-8'))
            
            elif message.startswith('!promote') and roles[clients[client_socket]] == 'admin':
                promote_user = message.split(' ')[1]
                if promote_user in clients.values():
                    roles[promote_user] = 'moderator'
                    client_socket.send(f"{promote_user} has been promoted to moderator.".encode('utf-8'))
                else:
                    client_socket.send(f"User {promote_user} not found.".encode('utf-8'))

            elif message.startswith('!demote') and roles[clients[client_socket]] == 'admin':
                demote_user = message.split(' ')[1]
                if demote_user in clients.values():
                    roles[demote_user] = 'user'
                    client_socket.send(f"{demote_user} has been demoted to user.".encode('utf-8'))
                else:
                    client_socket.send(f"User {demote_user} not found.".encode('utf-8'))
            
            elif message.startswith('@'):
                parts = message[1:].split(' ', 1)
                if len(parts) >= 2:
                    recipient_name = parts[0]
                    private_message = parts[1]

                    if recipient_name in blocked_users[username]:
                        client_socket.send(f"You have blocked {recipient_name}, you cannot send them messages.".encode('utf-8'))
                    else:
                        send_private_message(client_socket, recipient_name, private_message)
                else:
                    client_socket.send("Invalid private message format. Use @username message.".encode('utf-8'))
            
            elif message.lower() == 'exit':
                broadcast(f"{clients[client_socket]} has left the chat.", client_socket)
                print(f"{clients[client_socket]} disconnected.")
                break
            else:
                encrypted_message = caesar_cipher(message, 2)  
                broadcast(f"{clients[client_socket]}: {encrypted_message}", client_socket)
    except:
        pass
    finally:
        client_socket.close()
        if client_socket in clients:
            del clients[client_socket]
            del blocked_users[clients[client_socket]]
            del roles[clients[client_socket]]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print(f"Server started on {host}:{port}")

while True:
    client_socket, client_address = server.accept()
    print(f"New connection from {client_address}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
