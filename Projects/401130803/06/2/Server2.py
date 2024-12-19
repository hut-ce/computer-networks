import socket
import threading

clients = {}

def handle_client(CONNECTION, ADDR):

    print(f"Connected to {ADDR}")

    username = CONNECTION.recv(1024).decode('utf-8')
    clients[username] = CONNECTION
    print(f"{username}  joined the chat.")
    
    while True:
        Message = CONNECTION.recv(1024).decode('utf-8')
        if not Message:
            print(f"Connection with {ADDR} is closed")
            break

        # اگر پیام خصوصی باشد
        if Message.startswith('@'):
            target_user, private_message = Message[1:].split(" ", 1)
            if target_user in clients:
                clients[target_user].send(f"Private message from {username}: {private_message}".encode('utf-8'))
            else:
                CONNECTION.send(f"User {target_user} not found.".encode('utf-8'))
        else:
            broadcast(Message, CONNECTION, username)
    
    del clients[username]
    CONNECTION.close()

def broadcast(Message, CONNECTION, username):
    for client in clients.values():
        if client != CONNECTION:
            try:
                client.send(f"{username}: {Message}".encode('utf-8'))
            except:
                clients.remove(client)

def main():
    IP = socket.gethostbyname(socket.gethostname())
    Port = 5050

    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.bind((IP , Port))
    Server.listen()

    print("Server is Running!")

    while True:
        CONNECTION , ADDR = Server.accept()
        CONNECTION.send("Please enter your username:".encode('utf-8'))
        username = CONNECTION.recv(1024).decode('utf-8')
        
        thread = threading.Thread(target=handle_client , args=(CONNECTION , ADDR))
        thread.start()

if __name__ == "__main__":
    main()
