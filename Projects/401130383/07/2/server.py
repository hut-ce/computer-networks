import pickle
import socket
from threading import Thread
import os


def exe_command(client: 'socket.socket'):
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
                output = "This command Not valid!"
            client.send(pickle.dumps(output))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8080))
server.listen(10)
print('SERVER LISTENING on localhost:8080')

while True:
    client, addr = server.accept()
    print(f"Connect from this address {addr}")
    command = Thread(target=exe_command, args=(client,))
    command.start()
