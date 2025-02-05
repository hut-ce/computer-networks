import socket
import threading
import tkinter as tk
from tkinter import simpledialog

# Client configuration
HOST = '127.0.0.1'
PORT = 12345

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

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        self.shift = 3  # Caesar cipher shift value

        self.root = tk.Tk()
        self.root.title("Chatroom")

        self.messages_frame = tk.Frame(self.root)
        self.messages_frame.pack()

        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.msg_list = tk.Listbox(self.messages_frame, height=20, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()

        self.entry_field = tk.Entry(self.root, width=50)
        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.pack()

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.username = simpledialog.askstring("Username", "Enter your username:")
        self.client.send(self.username.encode('utf-8'))

        threading.Thread(target=self.receive_messages).start()

    def send_message(self, event=None):
        message = self.entry_field.get()
        if message:
            encrypted_message = caesar_cipher_encrypt(message, self.shift)
            self.client.send(encrypted_message.encode('utf-8'))
            self.entry_field.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                decrypted_message = caesar_cipher_decrypt(message, self.shift)
                self.msg_list.insert(tk.END, decrypted_message)
            except OSError:
                break

    def start(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self, event=None):
        self.client.close()
        self.root.quit()

if __name__ == "__main__":
    client = ChatClient()
    client.start()
