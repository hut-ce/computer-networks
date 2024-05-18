import socket
import threading

ip = '127.0.0.5'
port = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

name = input("Enter your name: \n")
def receive_messages(client):
    while True:
        message = client.recv(1024).decode('utf-8')
        print(message)

def send_messages(client):
    while True:
        message = input('enter your message: ')
        client.send(message.encode())
        if message.lower() == 'exit':
            break

client.send(name.encode())

receive_thread = threading.Thread(target=receive_messages, args=(client,))
send_thread = threading.Thread(target=send_messages, args=(client,))
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()

