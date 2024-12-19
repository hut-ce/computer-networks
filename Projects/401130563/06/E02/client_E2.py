import socket
import threading

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 55555))


def receive():
    """Receive messages from the server."""
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == 'NICK':
                client.send(nickname.encode("utf-8"))
            else:
                print(message)
        except:
            print('[ERROR] An error occurred')
            client.close()
            break


def write():
    """Send messages to the server."""
    while True:
        message = input()

        # Check for the '/pm' command
        if message.startswith('/pm '):
            try:
                _, recipient_nickname, private_message = message.split(' ', 2)
                client.send(message.encode('utf-8'))
            except ValueError:
                print('[ERROR] Invalid private message format. Use /pm [nickname] [message]')
        else:
            client.send(message.encode("utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
