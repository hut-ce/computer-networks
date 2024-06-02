import socket
import threading

# Server configuration
ip = '127.0.0.5'
port = 5050

# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))  # Bind the server to the specified IP and port
server.listen(5)  # Listen for incoming connections, with a backlog of 5

print("Server is Running and waiting for connections...")
# ---------------------Our Changes----------------------------
# Changing the list for clients to a dictionary
clients = {}
# Adding another dictionary for their names when needed to address them and their ports
client_names = {}
# -------------------------------------------------------------
def handle_client(connection, address):
    """
    Function to handle communication with a connected client.
    """
    try:
        name = connection.recv(1024).decode()  # Receive the client's name
        clients[name] = connection
        client_names[connection] = name

        print(f"{name} ({address}) is connected to the server!")
        # mode = "general"
        while True:
            message = connection.recv(1024).decode()  # Receive message from client

            if not message:  # If no message, break the loop
                break
            
            """ --------------------DISGRACE--------------------------
                if mode == "general":
                if message == "pv":
                    connection.send(clients.keys().encode())
                    mode = "pv"
                if mode == "pv":
                    if message in Client_names:
                -------------------------------------------------------""" 
            # -----------------Our Changes-------------------------------------------------
            if message.startswith("PRIVATE"): # changing the chat if it goes for a private
                _, recipient, private_message = message.split(": ", 2)
                if recipient in clients:
                    clients[recipient].send(f"PRIVATE: {name}: {private_message}".encode())
            #-------------------------------------------------------------------------------
            else:
                print(f"{name} ({address}) said {message}")
                # Broadcast the message to all other connected clients
                for client in clients.values():
                    if client != connection:
                        client.send(message.encode())
    except ConnectionResetError:
        print(f"Connection with {address} is closed.")
    finally: # for when the Client wants to get out of the chat.
        # Remove the client from the list and close the connection
        if connection in client_names:
            name = client_names[connection]
            del clients[name]
            del client_names[connection]
            connection.close()
            print(f"{name} ({address}) has left the chatroom!")

try:
    while True:
        connection, address = server.accept()  # Accept a new client connection
        # Create a new thread to handle the new client
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
except KeyboardInterrupt:
    print("Shutting down...")
    server.close()  # Close the server socket when exiting
