import socket
import ssl
import threading
HOST = '127.0.0.1'
PORT = 12345
CLIENT_CERT = 'client.crt'
CLIENT_KEY = 'client.key'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = ssl.wrap_socket(client_socket, keyfile=CLIENT_KEY, certfile=CLIENT_CERT, server_side=False)

client_socket.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode())
            else:
                break
        except:
            print("Connection lost.")
            break

def send_messages():
    while True:
        message = input("")
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode())

recv_thread = threading.Thread(target=receive_messages)
recv_thread.start()

send_messages()
