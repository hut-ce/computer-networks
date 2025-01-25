import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 55555))

while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        break
    print(data)

client_socket.close()
