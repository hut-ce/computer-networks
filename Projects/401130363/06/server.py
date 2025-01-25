import socket
import pickle
from threading import Thread

clients = {}
blocked_users = {}


def handle_client(client_socket: socket.socket, client_name: str):
    client_socket.send(pickle.dumps("Welcome to the server"))
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            content = pickle.loads(data)

            if isinstance(content, dict):
                if content["type"] == "PV":
                    user = content["target"]
                    if user:
                        if client_name not in blocked_users[user]:
                            clients[user].send(pickle.dumps({"PV": client_name, "message": content["message"]}))
                            print(f"Received PV message from {client_name}")
                        else:
                            client_socket.send(pickle.dumps("You are blocked by the recipient."))
                    else:
                        client_socket.send(pickle.dumps("Recipient not found."))

                elif content["type"] == "normal":
                    print(f"Received message from {client_name}")
                    broadcast(content["message"], client_name)

                elif content["type"] == "block":
                    blocked_users[client_name].add(content["target"])
                    client_socket.send(pickle.dumps(f"You have blocked {content['target']}."))

                elif content["type"] == "unblock":
                    blocked_users[client_name].discard(content["target"])
                    client_socket.send(pickle.dumps(f"You have unblocked {content['target']}."))
        except (ConnectionResetError, BrokenPipeError):
            break


def broadcast(message: str, sender_name: str):
    for name, client in clients.items():
        if name != sender_name:
            client.send(pickle.dumps({"sender": sender_name, "message": message}))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8080))
server.listen(10)
print('SERVER LISTENING on localhost:8080')

while True:
    client_socket, address = server.accept()
    client_name = pickle.loads(client_socket.recv(1024))
    clients[client_name] = client_socket
    blocked_users[client_name] = set()
    print(f"{client_name} connected from {address}")

    client_thread = Thread(target=handle_client, args=(client_socket, client_name))
    client_thread.start()
