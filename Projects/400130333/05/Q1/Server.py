import socket
import threading

IP = '127.0.0.1'
PORT = 5050
MAX_CLIENTS = 5

client = []

def handle_client(connection, address, name):
    while True:
        try:
            message = connection.recv(1024).decode('utf-8')
            if message:
                print(f'{name}: {message}')
                broadcast(f'{name}: {message}')
        except:
            index = client.index((connection, name))
            client.remove((connection, name))
            connection.close()
            print(f"{name} disconnected")
            broadcast(f"{name} left the chat.")
            break

def broadcast(message):
    for c in client:
        c[0].send(message.encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(MAX_CLIENTS)
    print(f'Server is Running on IP:{IP}|PORT:{PORT}')

    while True:
        connection, address = server.accept()
        print(f'New connection from {address}')

        connection.send("Type your message: \n".encode('utf-8'))
        name = connection.recv(1024).decode('utf-8')
        client.append((connection, name))

        broadcast(f'{name} joined the chat.')
        connection.send('You are now connected!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(connection, address, name))
        thread.start()

start_server()
