import socket
import pickle

host = '127.0.0.1'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
data = pickle.dumps(numbers)
client_socket.send(data)

sorted_numbers = pickle.loads(client_socket.recv(1024))
print(f'Sorted numbers: {sorted_numbers}')

client_socket.close()
