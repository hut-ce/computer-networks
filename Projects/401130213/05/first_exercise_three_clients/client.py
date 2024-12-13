import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP, PORT))


def receive_message(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Connection with the server is lost!")
            break
        except ConnectionAbortedError:
            break


thread = threading.Thread(target=receive_message, args=(client,))
thread.start()

try:
    while True:
        message = input("Type: \n")
        client.send(f"{message}".encode('utf-8'))
except KeyboardInterrupt:
    print("Connection is closing...")
    client.close()

