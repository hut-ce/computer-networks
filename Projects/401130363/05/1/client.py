import socket
import pickle

array = list(map(int, input().split()))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

data = pickle.dumps(array)
client_socket.send(data)

output = pickle.loads(client_socket.recv(1024))

for i,j in output.items():
    print(f'{i}: {j}')

client_socket.close()
