import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
Port = 5050

Client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
Client.connect((IP , Port))



while True:
    Message = input(print("Please Enter your Name:\n"))
    Client.send(Message.encode('utf-8'))

    