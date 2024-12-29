import socket
import threading

clients = []
usernames = []

def handle_client(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(f"{username}: {message}", client_socket)
            else:
                remove(client_socket)
                break
        except:
            continue

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

def remove(client_socket):
    index = clients.index(client_socket)
    clients.remove(client_socket)
    username = usernames[index]
    usernames.remove(username)
    broadcast(f"{username} left the chat.", client_socket)

def receive_connections(server_socket):
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection {address}.")
        
        client_socket.send("Enter your username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        
        clients.append(client_socket)
        usernames.append(username)
        
        print(f"Username {username}.")
        broadcast(f"{username} joined the chat.", client_socket)
        
        thread = threading.Thread(target=handle_client, args=(client_socket, username))
        thread.start()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 12345)) 
    server_socket.listen()
    print("Server is listening ...")
    
    receive_connections(server_socket)

if __name__ == "__main__":
    main()
