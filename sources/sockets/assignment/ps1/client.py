#!usr/bin/env python

import socket

host = "127.0.0.1"
port = 12023

c_socket = socket.socket()
c_socket.connect((host, port))

message = input("-> ")

while message.strip() != '!quit':
    c_socket.send(message.encode())
    s_data = c_socket.recv(1024).decode()

    print('<- ' + s_data)
    
    message = input("-> ")

c_socket.close()