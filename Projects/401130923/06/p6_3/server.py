import socket
import threading

host = '127.0.0.1'
port = 55555

clients = []
names = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                idx = clients.index(client)
                name = names[idx]
                broadcast(f'{name}: {message}'.encode('utf-8'), client)
        except:
            idx = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[idx]
            broadcast(f'{name} left the chat.'.encode('utf-8'), client)
            names.remove(name)
            break

def accept_clients():
    while True:
        client, addr = server.accept()
        print(f'Connected with {addr}')
        client.send('NAME'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        names.append(name)
        clients.append(client)

        print(f'Client name is {name}')
        broadcast(f'{name} joined the chat!'.encode('utf-8'), client)
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server is running...')
accept_clients()
