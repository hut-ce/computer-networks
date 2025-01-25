import socket
import ssl
import threading
HOST = '127.0.0.1'
PORT = 65432
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations('server.crt')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket = context.wrap_socket(client_socket, server_hostname=HOST)
secure_socket.connect((HOST, PORT))
print("Connected to secure chat server.")
def receive_messages():
    while True:
        try:
            message = secure_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Server: {message}")
        except:
            print("Connection lost.")
            break
threading.Thread(target=receive_messages, daemon=True).start()
try:
    while True:
        message = input("You: ")
        secure_socket.send(message.encode('utf-8'))
except:
    print("Disconnected.")
finally:
    secure_socket.close()
