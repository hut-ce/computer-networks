import socket
import threading

host = '127.0.0.1'
port = 55555

clients = []
usernames = []
roles = {}
blocked_users = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

def send_all(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def send_private(message, to_user, sender):
    if to_user in usernames:
        idx = usernames.index(to_user)
        recipient = clients[idx]
        sender_name = usernames[clients.index(sender)]
        if sender_name in blocked_users[to_user]:
            sender.send(f'You are blocked by {to_user}.'.encode('utf-8'))
        else:
            recipient.send(f'[Private] {sender_name}: {message}'.encode('utf-8'))
    else:
        sender.send('User not found.'.encode('utf-8'))

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('/private'):
                parts = message.split(' ', 2)
                to_user = parts[1]
                private_message = parts[2]
                send_private(private_message, to_user, client)
            elif message.startswith('/block'):
                parts = message.split(' ', 1)
                block_user = parts[1]
                user_name = usernames[clients.index(client)]
                if block_user in usernames:
                    blocked_users[user_name].append(block_user)
                    client.send(f'You have blocked {block_user}.'.encode('utf-8'))
                else:
                    client.send('User not found.'.encode('utf-8'))
            else:
                idx = clients.index(client)
                name = usernames[idx]
                send_all(f'{name}: {message}'.encode('utf-8'), client)
        except:
            idx = clients.index(client)
            clients.remove(client)
            client.close()
            name = usernames[idx]
            send_all(f'{name} left the chat.'.encode('utf-8'), client)
            usernames.remove(name)
            break

def accept_clients():
    while True:
        client, addr = server.accept()
        print(f'Connected with {addr}')
        client.send('USERNAME'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')

        usernames.append(name)
        clients.append(client)
        roles[name] = 'user'
        blocked_users[name] = []

        print(f'Username is {name}')
        send_all(f'{name} joined the chat!'.encode('utf-8'), client)
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server is running...')
accept_clients()
