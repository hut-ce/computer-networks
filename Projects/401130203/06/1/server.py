import socket
import threading
active_clients = []
usernames = []
def send_to_all(message):
    for client in active_clients:
        client.send(message)
def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024)
            send_to_all(msg)
        except:
            idx = active_clients.index(client_socket)
            active_clients.remove(client_socket)
            client_socket.close()
            username_left = usernames[idx]
            send_to_all(f"{username_left} has disconnected".encode("utf-8"))
            usernames.remove(username_left)
            break
def accept_clients():
    while True:
        client_socket, addr = server.accept()
        print("Connected with ", addr)
        client_socket.send("USERNAME".encode("utf-8"))
        username = client_socket.recv(1024).decode("utf-8")
        usernames.append(username)
        active_clients.append(client_socket)
        print(f"{username} joined the chat")
        send_to_all(f"{username} has joined!".encode("utf-8"))
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5050))
server.listen()

print("Server is listening...")
accept_clients()
