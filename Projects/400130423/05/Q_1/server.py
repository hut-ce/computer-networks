import socket
import threading

ip = '127.0.0.5'
port = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(5)
print('server is running...')

client = {}

def handle_client(connection, address):
    print(f'{address} is connected to the server...')
    name = connection.recv(1024).decode()
    client[connection] = name
    
    while True:
        message = connection.recv(1024).decode()
        if not message:
            break
        print(f'{client[connection]}: {message}')
        for item in client:
            if item != connection:
                item.send(f"{client[connection]}: {message}".encode())
    
while True:
    connection, address = server.accept()
    print(f"Accepted connection from {address[0]}:{address[1]}")
    
    client_thread = threading.Thread(target=handle_client, args=(connection, address))
    client_thread.start()

