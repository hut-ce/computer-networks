import socket
import threading

IP = '127.0.0.1'
PORT = 5050

def receive_messages(connection):
    while True:
        try:
            message = connection.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Error!")
            connection.close()
            break

def send_message(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    name = input("Enter your name: \n")
    client.send(name.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_message, args=(client,))
    send_thread.start()

start_client()
