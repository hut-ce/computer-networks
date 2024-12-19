import socket
import threading

host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

name = input("Enter your name: ")
client.send(name.encode('utf-8'))

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg != 'NAME':
                print(msg)
        except:
            print("Error occurred!")
            client.close()
            break

def send_messages():
    while True:
        msg = input("")
        client.send(msg.encode('utf-8'))

recv_thread = threading.Thread(target=receive_messages)
recv_thread.start()

write_thread = threading.Thread(target=send_messages)
write_thread.start()
