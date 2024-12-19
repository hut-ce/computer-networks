import socket
import threading
import tkinter as tk
from tkinter import messagebox

host = '127.0.0.1'  
port = 12345

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Room")
        self.root.geometry("400x600")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.username = tk.StringVar()
        self.username_label = tk.Label(self.root, text="Enter your username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, textvariable=self.username)
        self.username_entry.pack(pady=5)
        self.username_button = tk.Button(self.root, text="Join Chat", command=self.join_chat)
        self.username_button.pack(pady=5)

        self.chat_display = tk.Text(self.root, state=tk.DISABLED, height=20, width=50)
        self.chat_display.pack(pady=10)

        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(pady=5)
        self.message_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.message_button.pack(pady=5)

        self.receive_thread = None

    def join_chat(self):
        self.client_socket.send(self.username.get().encode('utf-8'))
        self.username_entry.config(state=tk.DISABLED)
        self.username_button.config(state=tk.DISABLED)

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                decrypted_message = caesar_cipher(message, -2) 
                self.display_message(decrypted_message)
            except:
                break

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END) 

    def send_message(self):
        message = self.message_entry.get()
        if message.lower() == 'exit':
            self.client_socket.send('exit'.encode('utf-8'))
            self.root.quit()
        else:
            encrypted_message = caesar_cipher(message, 2)  
            self.client_socket.send(encrypted_message.encode('utf-8'))
        self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chat_client = ChatClient(root)
    root.mainloop()