import socket
import threading

host = '127.0.0.1'
port = 55555

clients = []
names = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

def send_all(msg, sender):
    for client in clients:
        if client != sender:
            client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg:
                idx = clients.index(client)
                name = names[idx]
                send_all(f'{name}: {msg}'.encode('utf-8'), client)
        except:
            idx = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[idx]
            send_all(f'{name} left the chat.'.encode('utf-8'), client)
            names.remove(name)
            break

def receive_clients():
    while True:
        client, addr = server.accept()
        print(f'Connected with {addr}')
        client.send('NAME'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        names.append(name)
        clients.append(client)

        print(f'Client name is {name}')
        send_all(f'{name} joined the chat!'.encode('utf-8'), client)
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is running...')
receive_clients()
