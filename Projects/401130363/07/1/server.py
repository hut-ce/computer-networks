import socket
import threading

active_clients = []

def distribute_message(sender, message):
    for client in active_clients:
        if client.socket != sender:
            client.send(message)

class ClientConnection:
    def __init__(self, socket: socket.socket, address):
        self.socket = socket
        self.address = address

    def send(self, message):
        self.socket.sendall(message)

    def listen(self):
        with self.socket as client_socket:
            while True:
                try:
                    message = client_socket.recv(4096)
                    print(f"Received: {message}")
                    if not message:
                        break
                    distribute_message(sender=client_socket, message=message)
                except ConnectionResetError:
                    break
            print(f"Client {self.address} disconnected")
            active_clients.remove(self)

def initiate_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 2000))
        server_socket.listen()
        print("Server is listening on localhost:2000")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"New connection: {client_address}")
            new_client = ClientConnection(client_socket, client_address)
            active_clients.append(new_client)
            threading.Thread(target=new_client.listen).start()

if __name__ == '__main__':
    initiate_server()
