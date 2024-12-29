import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 55555))
server.listen()

clients = []
nicknames = []


def broadcast(message, sender_client=None):
    """Broadcast a message to all clients except the sender avoiding echo!"""
    for client in clients:
        if client != sender_client:  # avoid echoing the message back to the sender
            client.send(message)


def send_private_message(recipient_nickname, message, sender_nickname):
    """Send a private message to a specific user."""
    if recipient_nickname in nicknames:
        index = nicknames.index(recipient_nickname)
        recipient_client = clients[index]
        recipient_client.send(f'[PRIVATE] {sender_nickname}: {message}'.encode('utf-8'))
    else:
        sender_index = nicknames.index(sender_nickname)
        sender_client = clients[sender_index]
        sender_client.send(f'[ERROR] User {recipient_nickname} not found.'.encode('utf-8'))


def handle(client):
    """Handle incoming messages from a client."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                sender_index = clients.index(client)
                sender_nickname = nicknames[sender_index]

                # Check if the message is a private message
                if message.startswith('/pm '):
                    try:
                        # Extract the recipient's nickname and the message
                        _, recipient_nickname, private_message = message.split(' ', 2)
                        send_private_message(recipient_nickname, private_message, sender_nickname)
                    except ValueError:
                        client.send(
                            '[ERROR] Invalid private message format. Use /pm [nickname] [message]'.encode('utf-8'))
                else:
                    # Otherwise, broadcast the message to all clients
                    broadcast(f'{sender_nickname}: {message}'.encode('utf-8'), client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'[CHAT LEAVING] {nickname} has left the chat...'.encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    """Accept new client connections."""
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
