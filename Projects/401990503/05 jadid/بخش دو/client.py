
import socket
import threading

ip = "127.0.0.5"
port = 50600

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ip,port))

name = input("Please enter your name: ")
data = name
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



thread = threading.Thread(target=recieveMessage, args=(client,))
thread.start()

try:
    while True:
        message = input("Enter your numbers (Enter 0 to send):")
        if message == "0":
            client.send(data.encode("utf-8"))
            data = name
        else:
            data = data + f" {message}"
        
except KeyboardInterrupt:
    print(f"Keyboard intrupt on {name}. Connection closing...")
    client.close()