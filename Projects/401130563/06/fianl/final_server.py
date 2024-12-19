
"""
[NOTICE]
    this file is the final file for project 06 it
    contains all the features like Private Messaging,
    Blocking and Inappropriate Words Censoring(extra point part)

[features description]
    Private Message ==> /pm {client_name} {message}
    Blocking ==> /block {client_name}
    Inappropriate Word ==> add the word to the bad_words list in client file(final_client.py)
"""

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 55555))
server.listen()

clients = []
nicknames = []
blocked_users = {}  # Store blocked users for each nickname


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message.startswith('/pm '):  # Private message handling
                parts = message.split(' ', 2)
                recipient_nickname = parts[1]
                actual_message = parts[2]

                # Check if the sender is blocked by the recipient
                sender_nickname = nicknames[clients.index(client)]
                if recipient_nickname in blocked_users.get(sender_nickname, []):
                    client.send(
                        f'[ERROR] You are blocked by {recipient_nickname}. You cannot send private messages.'.encode(
                            'utf-8'))
                elif recipient_nickname in nicknames:
                    index = nicknames.index(recipient_nickname)
                    recipient_client = clients[index]
                    recipient_client.send(actual_message.encode('utf-8'))
                else:
                    client.send(f'[ERROR] User {recipient_nickname} not found.'.encode('utf-8'))

            elif message.startswith('/block '):  # Block command
                parts = message.split(' ', 1)
                blocked_nickname = parts[1]
                sender_nickname = nicknames[clients.index(client)]
                if blocked_nickname not in blocked_users:
                    blocked_users[blocked_nickname] = []
                blocked_users[blocked_nickname].append(sender_nickname)
                client.send(f'You have successfully blocked {blocked_nickname}.'.encode('utf-8'))

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
