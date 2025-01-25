import pickle
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 55555))

while True:
    comm = input("Enter your command:")
    if comm == 'exit':
        client_socket.send(pickle.dumps('0'))
        break

    client_socket.send(pickle.dumps(comm))

    result = client_socket.recv(1024 * 4)
    print(pickle.loads(result))
