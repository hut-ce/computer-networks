import socket

HOST = '127.0.0.1'
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    try:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

        if "Enter your move" in message:
            move = input("Your move (0-9): ")
            client_socket.sendall(move.encode('utf-8'))

    except:
        print("Connection lost.")
        break

client_socket.close()
