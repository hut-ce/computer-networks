import socket
import threading

ip = "127.0.0.3"
print(ip)
port = 5050
MAX_USERS = 5
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))

server.listen()

print("Server is Running and waiting for connections...")

clients = {}  
count = 0
def handle_client(connection, address):
    global count
    print(f"{address} is connected to the server!")

    count = count + 1
    print("pepeple join : ",count)
    if count > MAX_USERS:
        connection.send("Sorry, the chat room is full.".encode())
        connection.close()
        return
    
    
    username = connection.recv(1024).decode()
    clients[connection] = username
    print(f"{address} set the username to {username}")
    
    
    broadcast(f"{username} has joined the chatroom", connection)
    
    while True: 
        try: 
            message = connection.recv(1024).decode()

            if not message: 
                break 
            print(f"{username} said: {message}")

            broadcast(f"{username}: {message}", connection)
        except ConnectionResetError: 
            print(f"Connection with {address} is closed.")
            break 
    
    del clients[connection]
    connection.close()
    count = count-1
    print(f"{username} has left the chatroom!")
    broadcast(f"{username} has left the chatroom!", connection)

def broadcast(message, sender_connection):
    for client_socket in clients:
        if client_socket != sender_connection: 
            client_socket.send(message.encode())

try: 
    while True: 
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

except KeyboardInterrupt: 
    print("Shutting down...")
    server.close()
