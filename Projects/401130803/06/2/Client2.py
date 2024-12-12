import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
Port = 5050


Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Client.connect((IP, Port))


def listen_for_messages():
    while True:
        try:
            Message = Client.recv(1024).decode('utf-8')
            if Message:
                print(f"\n{Message}")
            else:
                print("Server connection closed.")
                break
        except:
            print("Error")
            break


thread = threading.Thread(target=listen_for_messages)
thread.daemon = True #اگر برنامه اصلی بسته شد
thread.start()

username = input("Enter your username:\n")
Client.send(username.encode('utf-8'))

while True:
    Message = input("Enter your message (use @username for private message):\n")
    
    if Message.lower() == 'exit':
        print("Disconnecting from the server...")
        Client.send("User has left the chat.".encode('utf-8'))
        Client.close()
        break
    
   
    Client.send(Message.encode('utf-8'))
