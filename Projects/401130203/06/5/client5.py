import socket
import threading
def recv_msgs():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(msg)
        except:
            print("Connection lost!")
            client.close()
            break
def send_msgs():
    while True:
        try:
            msg = input()
            client.send(msg.encode('utf-8'))
        except:
            print("Something went wrong!")
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("127.0.0.1", 5050))
except:
    print("Unable to connect to server!")
    exit()

username = input("Enter your username: ")
client.send(username.encode('utf-8'))

thread_recv = threading.Thread(target=recv_msgs)
thread_recv.start()

thread_send = threading.Thread(target=send_msgs)
thread_send.start()
