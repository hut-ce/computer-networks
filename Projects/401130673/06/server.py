import socket
import threading

clients = []
client_names = {}
client_roles = {}  
blocked_users = {}  

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except ConnectionResetError:
                print(f"sending message failed!")
                client.close()
                clients.remove(client)


def handle_client(client, address):
    name = client.recv(1024).decode('utf-8')
    role = client.recv(1024).decode('utf-8')
    
    client_names[client] = name
    client_roles[client] = role
    blocked_users[name] = []  

    welcome_message = f"{name} ({role}) has joined"
    print(welcome_message)
    broadcast(welcome_message.encode('utf-8'), client)
    
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break
            
            message_decoded = message.decode('utf-8')
            if message_decoded.startswith("@block"):
                _, blocked_name = message_decoded.split(" ", 1)
                if blocked_name in client_names.values():
                    blocked_users[name].append(blocked_name)
                    client.send(f"{blocked_name} has been blocked.".encode('utf-8'))
                else:
                    client.send(f"User {blocked_name} does not exist.".encode('utf-8'))
            elif message_decoded.startswith("@"):
                reciever, private_msg = message_decoded[1:].split(" ", 1)
                private_message(f"Private from {name}: {private_msg}".encode('utf-8'), name, reciever)
            else:
                broadcast(f"{name}: {message_decoded}".encode('utf-8'), client)
                print(f"{address} said {message}")
        except ConnectionResetError:
            print(f"connection with {address} is closed!")
            break

    client.close()
    clients.remove(client)
    goodbye = f"{name} ({role}) has left!"
    print(goodbye)
    broadcast(goodbye.encode('utf-8'), client)



def private_message(message, sender, reciever):
    for client, name in client_names.items():
        if name == reciever:
            if sender in blocked_users.get(name, []):
                try:
                    client.send(f"Message from user {sender} is blocked.".encode('utf-8'))
                    return True
                except ConnectionResetError:
                    print(f"sending private message failed!")
                    client.close()
                    clients.remove(client)
                    return False
            else:
                try:
                    client.send(message)
                    return True
                
                except ConnectionResetError:
                    print(f"sending private message failed!!")
                    client.close()
                    clients.remove(client)
                    return False
    return False




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5050))
server.listen(5)
print("Server is listening...")

try:
    while True:
        client, address = server.accept()
        clients.append(client)
        print(f"Accepted connection from {address}")
        thread=threading.Thread(target=handle_client, args=(client, address))
        thread.start()

except KeyboardInterrupt:
    print("shutting down...")
    server.close()