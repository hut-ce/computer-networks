import socket
from threading import Thread
import pickle
from caesar import caesar_encode, caesar_decode


class Client:
    def __init__(self, name, address, client_socket):
        self.name = name
        self.address = address
        self.client_socket = client_socket
        self.is_active = True

    def send(self, message: str):
        if self.is_active:
            encoded_message = caesar_encode(message, 7)
            data = pickle.dumps(encoded_message)
            self.client_socket.send(data)
            print(f'SENT: <{message}> to <{self.name}> - {self.address}')


clients = []


def client_handler(client_socket, address):
    with client_socket:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            decoded_message = pickle.loads(data)
            decoded_message = caesar_decode(decoded_message, 7)
            data_parts = decoded_message.split("`~`")
            print(f'RECEIVED: {data_parts} from {address}')

            if data_parts[0] == 'hello':
                for client in clients:
                    if client.name == data_parts[1]:
                        client.client_socket = client_socket
                        client.address = address
                        client.is_active = True
                        break
                else:
                    clients.append(Client(name=data_parts[1], address=address, client_socket=client_socket))

            elif data_parts[0] == 'message':
                for client in clients:
                    if client.name == data_parts[1]:
                        continue
                    client.send("`~`".join(data_parts))

            elif data_parts[0] == 'quit':
                for client in clients:
                    if client.name == data_parts[1]:
                        client.is_active = False
                        break
                print(f'DISCONNECTED: <{data_parts[1]}> - {address}')
                break
            else:
                for client in clients:
                    if client.name == data_parts[0]:
                        client.send("`~`".join(data_parts))


def server_program():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('127.0.0.1', 8080))
        server.listen(10)
        print('SERVER LISTENING on localhost:8080')
        while True:
            client_socket, address = server.accept()
            print(f'NEW CONNECTION: {address}')
            client = Thread(target=client_handler, args=(client_socket, address))
            client.start()


if __name__ == '__main__':
    server_program()
