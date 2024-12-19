import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 55555))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('/pm '):
                parts = message.split(' ', 2)
                recipient_nickname = parts[1]
                actual_message = parts[2]
                if recipient_nickname in nicknames:
                    index = nicknames.index(recipient_nickname)
                    recipient_client = clients[index]
                    recipient_client.send(actual_message.encode('utf-8'))
                else:
                    client.send(f'[ERROR] User {recipient_nickname} not found.'.encode('utf-8'))
            else:
                broadcast(message.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'[CHAT LEAVING] {nickname} has left the chat...'.encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'[CONNECTING] Connected with {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'[NICKNAME] Nickname of the client: {nickname}!')
        broadcast(f'[JOINING CHAT] {nickname} has joined the chat'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("[SERVER] Server is listening...")
receive()
