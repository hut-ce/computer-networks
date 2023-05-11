#!/usr/bin/env python
import socket


host = socket.gethostname()
port = 12021

s_socket = socket.socket()

s_socket.bind((host, port))

s_socket.listen(5)

conn, addr = s_socket.accept()

while True:
    r_data = conn.recv(1024).decode()
    if not r_data:
        break
    print('>>> ' + str(r_data))

    s_data = str(r_data)[::-1] # modify this line
    if s_data[-1].isupper():
        s_data = s_data[0].upper() + s_data[1:-1] + s_data[-1].lower()
    conn.send(s_data.encode())

s_socket.close()

