import socket
import ssl
import threading

SERVER_IP = "127.0.0.1"  
SERVER_PORT = 12345      


def receive_messages(ssl_socket):
    while True:
        try:
            message = ssl_socket.recv(1024).decode()
            print(message)
        except:
            print("[DISCONNECTED] Connection to server lost.")
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False  
    ssl_context.verify_mode = ssl.CERT_NONE  

    secure_socket = ssl_context.wrap_socket(client_socket)
    secure_socket.connect((SERVER_IP, SERVER_PORT))
    print("[CONNECTED] Connected to secure chat server.")

    
    threading.Thread(target=receive_messages, args=(secure_socket,)).start()

    
    while True:
        try:
            message = input()
            secure_socket.send(message.encode())
        except:
            print("[ERROR] Could not send message.")
            break

if __name__ == "__main__":
    start_client()
