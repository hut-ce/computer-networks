import pickle
import socket

server_host = '127.0.0.1'
server_port = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

while True:
    comm = input("Enter your command:")
    if comm == 'exit':
        client_socket.send(pickle.dumps('0'))
        break

    client_socket.send(pickle.dumps(comm))

    result = client_socket.recv(1024 * 4)
    print(pickle.loads(result))
