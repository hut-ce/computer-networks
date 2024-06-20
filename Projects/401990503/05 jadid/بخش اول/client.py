import socket
import threading

ip = "127.0.0.5"
port = 5060

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ip,port))

name = input("Please enter your name: ")
def introduceYS():
    massage = f"ClientName {name}"
    client.send(massage.encode("utf-8"))

def recieveMessage(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Connection with server is lost!")
            break

introduceYS()
thread = threading.Thread(target=recieveMessage,args=(client,))
thread.start()

try:
    while True:
        message = input("Enter your message: ")
        client.send(message.encode("utf-8"))
except KeyboardInterrupt:
    print("Keyboard intrupt. Connection closing...")
    client.close()
