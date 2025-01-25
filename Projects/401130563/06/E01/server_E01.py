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
            message = client.recv(1024)
            broadcast(message)
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
        client.send('Connected to the server!'.encode('utf-8'))
        broadcast(f'[JOINING CHAT] {nickname} has joined the chat'.encode('utf-8'))


        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("[SERVER] Server is listening...")
receive()
