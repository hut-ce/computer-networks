import socket
import threading

ip = "127.0.0.5"
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))

server.listen(5)

print("Server is Running and waiting for connections...")

client = []

def handle_client(connection, address):
    print(f"{address} is connected to the server!")
    while True: 
        try: 
            message = connection.recv(1024).decode()

            if not message: 
                break 
            print(f"{address} said {message}")

            for c in client:
                if c != connection: 
                    c.send(message.encode())
        except ConnectionResetError: 
            print(f"Connection with {address} is closed. ")

            break 
    
    client.remove(connection)
    connection.close()
    print(f"{address} has left the chatroom!")

try: 
    while True: 
        connection, address = server.accept()
        client.append(connection)
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

except KeyboardInterrupt: 
    print("Shutting down...")
    server.close()
    