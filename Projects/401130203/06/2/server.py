import socket
import threading

active_clients = []
usernames = []
def send_to_user(target_user, message):
    if target_user in usernames:
        target_index = usernames.index(target_user)
        target_client = active_clients[target_index]
        target_client.send(message.encode('utf-8'))
def send_to_all(message):
    for client in active_clients:
        client.send(message.encode('utf-8'))
def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg.startswith("/pm"):
                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    client_socket.send("Invalid private message format. Use: /pm <username> <message>".encode('utf-8'))
                else:
                    target_user = parts[1]
                    private_message = parts[2]
                    sender_index = active_clients.index(client_socket)
                    sender_username = usernames[sender_index]
                    send_to_user(target_user, f"[Private] {sender_username}: {private_message}")
            else:
                sender_index = active_clients.index(client_socket)
                sender_username = usernames[sender_index]
                send_to_all(f"{sender_username}: {msg}")
        except:
            idx = active_clients.index(client_socket)
            active_clients.remove(client_socket)
            client_socket.close()
            user_left = usernames[idx]
            usernames.remove(user_left)
            send_to_all(f"{user_left} has left the chat.")
            break
def accept_clients():
    while True:
        client_socket, addr = server.accept()
        print(f"Connected with {addr}")
        client_socket.send("USERNAME".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        usernames.append(username)
        active_clients.append(client_socket)
        print(f"{username} joined the chat.")
        send_to_all(f"{username} has joined the chat.")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5050))
server.listen()
print("Server is listening...")
accept_clients()
