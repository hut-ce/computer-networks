import socket
import pickle

host = '127.0.0.1'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print('Server is listening...')

client_socket, addr = server_socket.accept()
print(f'Connection from {addr}')

data = client_socket.recv(1024)
numbers = pickle.loads(data)
print(f'Received numbers: {numbers}')

sorted_numbers = sorted(numbers)
client_socket.send(pickle.dumps(sorted_numbers))

client_socket.close()
server_socket.close()



