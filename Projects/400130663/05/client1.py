import socket
import threading

ip = '127.0.0.1'
port = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket

try:
    client.connect((ip, port))  # Connect to the server at the specified IP and port
except ConnectionRefusedError:
    print("Connection failed! The server might be down or unreachable.")
    exit()

name = input("Please enter your username: \n")  # Get username from input

# Create a dictionary to store username-message pairs
username_message_dict = {}

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Connection with server is lost!")
            break

thread = threading.Thread(target=receive_messages, args=(client,))  # Pass the client socket
thread.start()

try:
    while True:
        message = input("Type your message: \n")  # Get message from input
        # Prepend username to the message
        formatted_message = f"{name}: {message}"
        # Send the formatted message to the server
        client.send(formatted_message.encode('utf-8'))
except KeyboardInterrupt:
    print("Connection is getting closed. ")

client.close()  # Close the socket connection
