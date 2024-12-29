import socket
from threading import Thread
from caesar import caesar_encode, caesar_decode


class Client:
    def __init__(self, name, address, client_socket):
        self.name = name
        self.address = address
        self.client_socket = client_socket
        self.is_active = True

    def send(self, message: str):
        if self.is_active:
            self.client_socket.send(caesar_encode(message, 11).encode())
            print(f'SENT: <{message}> to <{self.name}> - {self.address}')


clients = []


def client_handler(client_socket, address):
    with client_socket:
        while True:
            data = client_socket.recv(1024).decode()
            data = caesar_decode(data, 11).split("`~`")
            print(f'RECEIVED: {data} from {address}')

            if data[0] == 'hello':
                for client in clients:
                    if client.name == data[1]:
                        client.client_socket = client_socket
                        client.address = address
                        client.is_active = True
                        # break
                else:
                    clients.append(Client(name=data[1], address=address, client_socket=client_socket))

            elif data[0] == 'message':
                for client in clients:
                    if client.name == data[1]:
                        continue
                    client.send("`~`".join(data))

            elif data[0] == 'quit':
                for client in clients:
                    if client.name == data[1]:
                        client.is_active = False
                        break
                print(f'DISCONNECTED: <{data[1]}> - {address}')
                break
            else:
                for client in clients:
                    if client.name == data[0]:
                        client.send("`~`".join(data))


# message form: head`~`name`~`data
def server_program():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('127.0.0.1', 8070))
        server.listen(10)
        print('SERVER LISTENING on localhost:8070')
        while True:
            client_socket, address = server.accept()
            print(f'NEW CONNECTION: {address}')
            client = Thread(target=client_handler, args=(client_socket, address))
            client.start()


if __name__ == '__main__':
    server_program()
