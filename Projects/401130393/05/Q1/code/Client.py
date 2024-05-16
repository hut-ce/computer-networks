import socket
import threading

ip = '127.0.0.5'
port = 5050 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

name = input("Enter your name:\n")
client.send(name.encode('utf-8'))

def receive_message(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Connection with server is lost!")
            break
        
thread = threading.Thread(target=receive_message, args=(client,))
thread.start()

try:
    while True:
        message = input("Type: \n")
        client.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("Connection is getting closed.")
    client.close()