import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 10000))

name = input("Enter your name: ")
client_socket.send(name.encode('utf-8'))

threading.Thread(target=receive_messages, args=(client_socket,)).start()

while True:
    message = input()
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode('utf-8'))

client_socket.close()

#for private message, must start the message with an @
