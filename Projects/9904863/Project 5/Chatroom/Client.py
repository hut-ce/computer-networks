import socket
import threading

ip="127.0.0.2"
port=5050
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ip,port))

name=input("Enter Your Username \n")
client.send(name.encode('utf-8'))
print("Now You Can Type: \n")

while True:
    message=input()
    client.send(message.encode('utf-8'))
    if message.lower()=='exit':
        break
