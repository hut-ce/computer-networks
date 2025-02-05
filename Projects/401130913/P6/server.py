import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Arbitrary non-privileged port

def caesar_cipher_encrypt(message, shift):
    encrypted = ''
    for char in message:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted += char
    return encrypted

def caesar_cipher_decrypt(message, shift):
    return caesar_cipher_encrypt(message, -shift)

class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()
        print(f"Server running on {HOST}:{PORT}")

        self.clients = {}
        self.user_roles = {}
        self.blocked_users = {}
        self.offensive_words = ["badword1", "badword2"]

    def broadcast(self, message, sender):
        for client, username in self.clients.items():
            if client != sender:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.disconnect_client(client)

    def handle_client(self, client):
        try:
            username = client.recv(1024).decode('utf-8')
            self.clients[client] = username
            self.blocked_users[username] = []
            self.user_roles[username] = 'User'  # Default role
            print(f"{username} has joined the chat.")
            self.broadcast(f"{username} has joined the chat!", client)

            while True:
                message = client.recv(1024).decode('utf-8')
                if message.startswith("/pm"):
                    self.private_message(client, message)
                elif message.startswith("/block"):
                    self.block_user(client, message)
                elif message.startswith("/admin"):
                    self.admin_command(client, message)
                else:
                    self.process_message(client, message)
        except:
            self.disconnect_client(client)

    def process_message(self, client, message):
        username = self.clients[client]
        if any(word in message for word in self.offensive_words):
            client.send("Your message contains offensive language and was not sent.".encode('utf-8'))
            return
        print(f"{username}: {message}")
        self.broadcast(f"{username}: {message}", client)

    def private_message(self, client, message):
        username = self.clients[client]
        _, recipient, *msg_content = message.split()
        recipient_message = ' '.join(msg_content)

        for recipient_client, recipient_username in self.clients.items():
            if recipient_username == recipient and username not in self.blocked_users[recipient]:
                recipient_client.send(f"[PM from {username}]: {recipient_message}".encode('utf-8'))
                return
        client.send(f"Cannot send message to {recipient}. You might be blocked.".encode('utf-8'))

    def block_user(self, client, message):
        username = self.clients[client]
        _, target_user = message.split()
        self.blocked_users[username].append(target_user)
        client.send(f"You have blocked {target_user}.".encode('utf-8'))

    def admin_command(self, client, message):
        username = self.clients[client]
        if self.user_roles[username] != 'Admin':
            client.send("You do not have admin privileges.".encode('utf-8'))
            return

        if message.startswith("/admin kick"):
            _, _, target_user = message.split()
            for target_client, target_username in self.clients.items():
                if target_username == target_user:
                    target_client.send("You have been kicked by an admin.".encode('utf-8'))
                    self.disconnect_client(target_client)
                    break

    def disconnect_client(self, client):
        username = self.clients.pop(client, None)
        if username:
            self.broadcast(f"{username} has left the chat.", client)
            print(f"{username} disconnected.")
        client.close()

    def start(self):
        while True:
            client, address = self.server.accept()
            print(f"Connection from {address}.")
            threading.Thread(target=self.handle_client, args=(client,)).start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
