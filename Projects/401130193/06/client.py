import socket
import threading

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


class ChatClient:
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=5050):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def listen(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message.startswith("Private from"):
                    _, temp , sender, *msg = message.split()
                    decrypted_msg = caesar_decrypt(' '.join(msg), 3)
                    print(f"Private from {sender} {decrypted_msg}")
                else:
                    print(message)
            except Exception as e:
                print(f"Connection to server lost: {e}")
                break

    def send(self):
        while True:
            message = input()
            self.client.send(message.encode('utf-8'))

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        self.send()


if __name__ == "__main__":
    client = ChatClient()
    client.start()
