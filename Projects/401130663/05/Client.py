import socket
import threading

IP = '127.0.66.1'
PORT = 4066
Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect((IP, PORT))
Client_Name = input("Please type your name: ")
Client.send(Client_Name.encode("utf-8"))

def Recieve_Message(Client):
    while True:
        try:
            Message = Client.recv(1024).decode("utf-8")
            if not Message:
                break
            print("\n", Message)
        except ConnectionResetError:
            print("Your Connection to the server is severed.")
            break

threading.Thread(target=Recieve_Message, args=(Client,)).start()
try:
    while True:
        Message = input(f"{Client_Name}:")
        Client.send(Message.encode("utf-8"))
except KeyboardInterrupt:
    print(f"{Client_Name}'s connection is closed.")
    Client.close()