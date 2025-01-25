import socket
import threading

clients = []


def broadcast(sender_client, data):
    for client in clients:
        if client.client_socket != sender_client:
            client.send(data)


class Client:
    def __init__(self, client_socket: socket.socket, address):
        self.client_socket = client_socket
        self.address = address

    def send(self, data):
        self.client_socket.sendall(data)

    def handle(self):
        with self.client_socket as client_socket:
            while True:
                try:
                    data = client_socket.recv(4096)
                    print(f'[RECEIVED] received data {data}')
                    if not data:
                        break
                    broadcast(sender_client=client_socket, data=data)
                except ConnectionResetError:
                    break
            print(f'[CONECTION] connection lost: {self.address}')
            clients.remove(self)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('localhost', 55555))
    server.listen()
    print('[LISTENING] server is listening...!')

    while True:
        client_socket, addr = server.accept()
        print(f'[CONNECTION] connection address: {addr[1]}')
        client = Client(client_socket, addr)
        clients.append(client)
        threading.Thread(target=client.handle, args=()).start()
