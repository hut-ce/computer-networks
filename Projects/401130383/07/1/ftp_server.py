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
                    print(f'received {data}')
                    if not data:
                        break
                    broadcast(sender_client=client_socket, data=data)
                except ConnectionResetError:
                    break
            print(f'CLIENT DISCONNECTED: {self.address}')
            clients.remove(self)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('127.0.0.1', 2000))
        server.listen()
        print('SERVER LISTENING on localhost:2000')

        while True:
            client_socket, address = server.accept()
            print(f'NEW CONNECTION: {address}')
            client = Client(client_socket, address)
            clients.append(client)
            threading.Thread(target=client.handle, args=()).start()


if __name__ == '__main__':
    start_server()

