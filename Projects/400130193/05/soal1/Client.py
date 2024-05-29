import socket
import threading

ip = "127.0.0.3"
port = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((ip, port))
except ConnectionRefusedError:
    print("Unable to connect to the server. Please try again later.")
    exit()



name = input("Please enter your name: \n")
client.send(name.encode())

def receive_message(client):
    while True: 
        try: 
            message = client.recv(1024).decode()
            if not message: 
                break
            print(message)
        except ConnectionResetError:
            print("Connection with server is lost!")
            break
        except ConnectionAbortedError:
            print("Chat room is full. Please try again later.")
            break

thread = threading.Thread(target=receive_message, args=(client,))
thread.start()

try: 
    while True: 
        message = input("Type: \n")
        client.send(message.encode('utf-8'))  
except KeyboardInterrupt: 
    print("Connection is getting closed. ")
    client.close()
