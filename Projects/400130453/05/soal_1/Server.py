import socket
import threading

ip = '127.0.0.3'
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))

server.listen(5)

print("Server is Running and waiting for connections...")

client = []
names = {}


def handle_client(connection, address):
    print(f"{names[connection]} is joined to the chatroom!")
    while True: 
        try: 
            message = connection.recv(1024).decode('utf-8')
            
            if not message: 
                break 
            print(f"{names[connection]} said {message}")
            
            for c in client:
                if c != connection: 
                    c.send((f"{names[connection]}: {message}").encode('utf-8'))
        except ConnectionResetError: 
            print(f"{names[connection]} has left the chatroom. ")
            break 
    
    client.remove(connection)
    connection.close()
    print(f"{names[connection]} has left the chatroom!")
    for c in client:
        if c != connection: 
            c.send((f"{names[connection]} has left the chatroom!").encode('utf-8'))

def handle_names(connection):
    name = connection.recv(1024).decode('utf-8')
    names[connection] = name 

try: 
    while True: 
        connection, address = server.accept()
        client.append(connection)
        handle_names(connection)
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

except KeyboardInterrupt: 
    print("Shutting down...")
    server.close()