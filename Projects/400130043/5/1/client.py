# client
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

def main():
    client_name = input("Enter your name: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(client_name.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        client_socket.sendall(message.encode('utf-8'))

if name == "main":
    main()