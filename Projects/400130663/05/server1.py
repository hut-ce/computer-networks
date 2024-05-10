import socket
import threading

ip = '127.0.0.1'
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(5)
print("Server is Running and waiting for connections...")
client_list = []  # Store connected clients

def handle_client(connection, address):
    print(f"{address} is connected to the server!")
    while True:
        try:
            message = connection.recv(1024).decode('utf-8')
            if not message:
                break
            # Extract username and message from the received message
            username, message_content = message.split(':')
            # Prepend username to the message
            formatted_message = f"{username}: {message_content}"
            print(f"{address} said {message}")
            # Broadcast the formatted message to all connected clients
            for c in client_list:
                if c != connection:
                    c.send(formatted_message.encode('utf-8'))
        except (ConnectionResetError, ConnectionError) as e:
            print(f"Connection with {address} is closed: {e}")
            break

    client_list.remove(connection)
    connection.close()
    print(f"{address} has left the chatroom!")

try:
    while True:
        connection, address = server.accept()
        client_list.append(connection)
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    server.close()
