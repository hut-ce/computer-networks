import socket
import ssl
import threading

ip = "127.0.0.1"  
port = 12345      

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    ssl_contx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_contx.check_hostname = False  
    ssl_contx.verify_mode = ssl.CERT_NONE  

    secure_socket = ssl_contx.wrap_socket(client_socket)
    secure_socket.connect((ip, port))
    print("[CONNECTED] Connected to secure chat server.")

    
    threading.Thread(target=receive_messages, args=(secure_socket,)).start()

    
    while True:
        try:
            message = input()
            secure_socket.send(message.encode())
        except:
            print("[ERROR] Could not send message.")
            break

def receive_messages(ssl_socket):
    while True:
        try:
            message = ssl_socket.recv(1024).decode()
            print(message)
            
        except:
            print("[DISCONNECTED] Connection to server lost.")
            break

if __name__ == "__main__":
    start_client()
