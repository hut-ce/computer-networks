import socket
import threading

ip = '127.0.0.10'
port = 5050

def receive_message(conn):
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Oops! Failed.")
            conn.close()
            break

def send_message(client):
    while True:
        message = input()
        client.send(message.encode('utf-8'))

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    name = input("Name: ")
    client.send(name.encode('utf-8'))

    recv_thread = threading.Thread(target=receive_message, args=(client,))
    recv_thread.start()

    send_thread = threading.Thread(target=send_message, args=(client,))
    send_thread.start()

start_client()
