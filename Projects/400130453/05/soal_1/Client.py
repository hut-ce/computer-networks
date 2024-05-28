import socket
import threading

ip = "127.0.0.3"
port = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((ip, port))

name = input("Please enter your name: \n")
print("Chat with your friends and enjoy")

def receive_message(client):
    while True: 
        try: 
            message = client.recv(1024).decode()
            if not message: 
                break
            print(f"{message}")
        except ConnectionResetError:
            print("Connection with server is lost!")
            break

thread = threading.Thread(target=receive_message, args=(client,))
thread.start()
try: 
    client.send(name.encode('utf-8'))
    while True: 
        message = input()
        client.send((f"{message}").encode('utf-8'))
except KeyboardInterrupt: 
    print("Connection is getting closed. ")
    client.close()
