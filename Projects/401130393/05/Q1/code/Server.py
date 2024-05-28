import socket
import threading

ip = '127.0.0.5'
port = 5050 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(5)

print("Server is Running and waiting for connections...")

clients = []

def handle_clients(connection):
    name = connection.recv(1024).decode('utf-8')
    print(f"{name} has joined the chatroom!")
    
    while True:
        try:
            message = connection.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast_message = f"{name}: {message}"
            print(broadcast_message)
            
            for c in clients:
                if c != connection:
                    c.send(broadcast_message.encode('utf-8'))
            
        except ConnectionResetError:
            print(f"Connection with {name} is closed.")
            break 
        
    clients.remove(connection)
    connection.close()
    print(f"{name} has left the chatroom!")

try:
    while True:
        connection, address = server.accept()
        clients.append(connection)
        thread = threading.Thread(target=handle_clients, args=(connection,))
        thread.start()
        
except KeyboardInterrupt:
    print("Server is shutting down...")
    server.close()

