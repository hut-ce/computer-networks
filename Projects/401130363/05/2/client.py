import socket
import pickle

# array = list(map(int, input().split()))
array = [1, 5, 4, 6, 9,]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

data = pickle.dumps(array)
client_socket.send(data)

output = pickle.loads(client_socket.recv(1024))
fast = pickle.loads(client_socket.recv(1024))

for i, j in output.items():
    print(f'{i}: {j[0]} time:{j[1]}')

print("fastest:", fast)

client_socket.close()
