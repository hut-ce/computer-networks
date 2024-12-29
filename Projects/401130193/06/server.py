import socket
import threading
from collections import defaultdict


# Encryption and decryption using Caesar Cipher
def caesar_encrypt(message, key):
    encrypted = ""
    for char in message:
        if char.isalpha():
            shift = key % 26
            base = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted += char
    return encrypted


def caesar_decrypt(message, key):
    return caesar_encrypt(message, -key)


class ChatServer:
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=5050):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server started on {host}:{port}")

        self.clients = {}
        self.usernames = {}
        self.block_list = defaultdict(set)

    def broadcast(self, message, sender=None):
        for client, username in self.clients.items():
            if sender and username in self.block_list[sender]:
                continue
            client.send(message.encode('utf-8'))

    def handle_client(self, client):
        try:
            client.send("Enter your username: ".encode('utf-8'))
            username = client.recv(1024).decode('utf-8').strip()

            if not username:
                client.send("Invalid username. Connection closing.".encode('utf-8'))
                client.close()
                return

            self.clients[client] = username
            self.usernames[username] = client
            print(f"{username} joined the chat")
            guid = '----------------------------------------------------------------------------\n'
            guid += ("[MESSAGE] -> Send MESSAGE in public chat\n" +
                     "/private [USERNAME] [MESSAGE] -> Send private MESSAGE for USERNAME in PV\n" +
                     "/block [USERNAME] -> To block USERNAME in PV\n" +
                     "/unblock [USERNAME] -> To unblock USERNAME in PV\n")
            guid += '----------------------------------------------------------------------------\n'
            self.broadcast(f"{username} joined the chat!\n{guid}", sender=username)

            while True:
                message = client.recv(1024).decode('utf-8').strip()

                if message.startswith("/private"):
                    _, target_user, *private_msg = message.split()
                    private_msg = ' '.join(private_msg)
                    if target_user in self.block_list[username]:
                        client.send("User has blocked you.".encode('utf-8'))
                        continue
                    if username in self.block_list[target_user]:
                        client.send("You blocked user.".encode('utf-8'))
                        continue
                    if target_user in self.usernames:
                        encrypted_msg = caesar_encrypt(private_msg, 3)
                        self.usernames[target_user].send(f"Private from {username}: {encrypted_msg}".encode('utf-8'))
                    else:
                        client.send("User not found.".encode('utf-8'))

                elif message.startswith("/block"):
                    _, target_user = message.split()
                    self.block_list[target_user].add(username)
                    client.send(f"Blocked {target_user}.".encode('utf-8'))

                elif message.startswith("/unblock"):
                    _, target_user = message.split()
                    self.block_list[target_user].discard(username)
                    client.send(f"Unblocked {target_user}.".encode('utf-8'))

                else:
                    encrypted_msg = caesar_encrypt(message, 3)
                    self.broadcast(f"{username}: {encrypted_msg}", sender=username)

        except:
            pass
        username = self.clients.pop(client, None)
        if username:
            print(f"{username} left the chat")
            self.broadcast(f"{username} left the chat!", sender=username)
        client.close()

    def start(self):
        while True:
            client, _ = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()


if __name__ == "__main__":
    server = ChatServer()
    server.start()