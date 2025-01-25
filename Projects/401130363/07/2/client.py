import pickle
import socket

server_address = '127.0.0.1'
server_port = 1234
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_address, server_port))

while True:
    command = input("Enter your command: ")
    if command == 'exit':
        client.send(pickle.dumps('0'))
        break

    client.send(pickle.dumps(command))

    response = client.recv(1024 * 10)
    print(pickle.loads(response))
