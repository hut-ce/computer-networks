import socket
import threading
from tkinter import Tk, Text, Entry, Button, END


class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print("Server started on", host, ":", port)

        self.clients = {}
        self.banned_words = ["badword1", "badword2"] 

    def broadcast(self, message, sender=None):
        for client, name in self.clients.items():
            if client != sender:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client)

    def send_private(self, sender, recipient_name, message):
        recipient = None
        for client, name in self.clients.items():
            if name == recipient_name:
                recipient = client
                break
        if recipient:
            try:
                sender_name = self.clients[sender]
                recipient.send(f"[Private from {sender_name}]: {message}".encode('utf-8'))
            except:
                self.remove_client(recipient)
        else:
            sender.send(f"User {recipient_name} not found.".encode('utf-8'))

    def remove_client(self, client):
        if client in self.clients:
            name = self.clients.pop(client)
            print(f"{name} disconnected")

    def filter_message(self, message):
        for word in self.banned_words:
            message = message.replace(word, "***")
        return message

    def handle_client(self, client):
        name = client.recv(1024).decode('utf-8')
        self.clients[client] = name
        print(f"{name} connected")
        self.broadcast(f"{name} has joined the chat!", sender=client)

        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                if message.startswith("/private"):
                    parts = message.split(" ", 2)
                    if len(parts) == 3:
                        _, recipient_name, private_message = parts
                        self.send_private(client, recipient_name, private_message)
                    else:
                        client.send("Invalid private message format. Use /private <username> <message>.".encode('utf-8'))
                else:
                    message = self.filter_message(message)
                    self.broadcast(f"{name}: {message}", sender=client)
            except:
                break

        self.remove_client(client)
        self.broadcast(f"{name} has left the chat.")
        client.close()

    def start(self):
        while True:
            client, addr = self.server.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client,)).start()



class ChatClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.gui_done = False
        self.running = True

        self.gui_thread = threading.Thread(target=self.gui_loop)
        self.receive_thread = threading.Thread(target=self.receive)

        self.gui_thread.start()
        self.receive_thread.start()

    def gui_loop(self):
        self.win = Tk()
        self.win.title("Chat Room")

        self.chat_area = Text(self.win)
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state='disabled')

        self.msg_entry = Entry(self.win)
        self.msg_entry.pack(padx=20, pady=5)

        self.send_button = Button(self.win, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        message = self.msg_entry.get()
        self.client.send(message.encode('utf-8'))
        self.msg_entry.delete(0, END)

    def stop(self):
        self.running = False
        self.client.close()
        self.win.destroy()

    def receive(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if self.gui_done:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(END, message + "\n")
                    self.chat_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except Exception as e:
                print("Error:", e)
                break


if __name__ == "__main__":
    choice = input("Run as server (s) or client (c)? ").lower()
    if choice == 's':
        server = ChatServer()
        server.start()
    elif choice == 'c':
        name = input("Enter your name: ")
        client = ChatClient()
        client.client.send(name.encode('utf-8'))
