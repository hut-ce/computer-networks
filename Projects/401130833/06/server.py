import socket
import threading


class User:
    def __init__(self, ID, role, connection, address):
        self.roles = ["user", "admin", "manager"]
        self.name = ""
        self.ID = ID
        self.role = role if role in self.roles else "user"
        self.connection = connection
        self.address = address
        self.blocked_names = []
        self.is_blocked_by = []

    def block_name(self, name):
        if name not in self.blocked_names:
            self.blocked_names.append(name)

    def unblock_name(self, name):
        if name in self.blocked_names:
            self.blocked_names.remove(name)

    def send_message(self, message):
        try:
            self.connection.send(message.encode("utf-8"))
        except ConnectionResetError:
            print(f"Connection to {self.name} lost.")

    def __str__(self):
        return f"User(name={self.name}, ID={self.ID}, role={self.role})"


class Chatroom:
    def __init__(self):
        self.clients = []
        self.connections = []
        self.next_ID = 0

    def add_client(self, user):
        self.clients.append(user)
        self.connections.append(user.connection)

    def remove_client(self, user):
        self.clients.remove(user)
        self.connections.remove(user.connection)

    def find_user_by_name(self, name):
        for client in self.clients:
            if client.name == name:
                return client
        return None

    def broadcast_message(self, sender, message):
        for client in self.clients:
            if client.name != sender.name and sender.name not in client.blocked_names:
                client.send_message(f"{sender.name}: {message}")

    def private_message(self, sender, recipient_name, message):
        recipient = self.find_user_by_name(recipient_name)
        if recipient:
            if sender.name in recipient.blocked_names:
                sender.send_message("You are blocked by this user.")
            else:
                recipient.send_message("Private message incoming...")
                recipient.send_message(message)
        else:
            sender.send_message("User not found.")

    def handle_client(self, user):
        connection = user.connection
        try:
            while True:
                command = connection.recv(1024).decode()
                if command == "send":
                    message = connection.recv(1024).decode()
                    self.broadcast_message(user, message)
                elif command == "block":
                    name = connection.recv(1024).decode()
                    user.block_name(name)
                elif command == "unblock":
                    name = connection.recv(1024).decode()
                    user.unblock_name(name)
                elif command == "private message":
                    recipient_name = connection.recv(1024).decode()
                    message = connection.recv(1024).decode()
                    self.private_message(user, recipient_name, message)
                elif command == "quit":
                    break
        finally:
            self.remove_client(user)
            connection.close()

    def start(self, server):
        print("Server is running...")
        while True:
            connection, address = server.accept()
            print(f"New connection from {address}")
            user = User(self.next_ID, "user", connection, address)
            self.next_ID += 1
            user.name = connection.recv(1024).decode()
            self.add_client(user)
            threading.Thread(target=self.handle_client, args=(user,)).start()


def profanity_filter(message):
    profanity_list = ["badword1", "badword2", "badword3"]  # Example words
    for word in profanity_list:
        message = message.replace(word, "***")
    return message


IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(5)

chatroom = Chatroom()
chatroom.start(server_socket)
