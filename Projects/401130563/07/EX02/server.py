import pickle
import socket
from threading import Thread
import os


def command(client: 'socket.socket'):
    while True:
        data = client.recv(1024)
        if data:
            comm = pickle.loads(data)
            if comm == '0':
                client.close()
                break
            stream = os.popen(comm)
            output = stream.read()
            if output == "":
                output = "This command IS NOT valid!!"
            client.send(pickle.dumps(output))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 55555))
server.listen()
print('[LISTENING] server is listening...!')

while True:
    client, address = server.accept()
    print(f'[CONNECTION] connection address: {address}')
    command = Thread(target=command, args=(client,))
    command.start()
