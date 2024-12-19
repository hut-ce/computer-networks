import socket
import threading

host = '127.0.0.1' 
port = 12345

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from the server.")
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print("Connected to the chat room!")

username = input("Enter your username: ")
client.send(username.encode('utf-8'))

thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()

while True:
    message = input()
    if message.lower() == 'exit':
        client.close()
        break
    elif message.startswith('@'):
        client.send(message.encode('utf-8'))
    else:
        client.send(message.encode('utf-8'))