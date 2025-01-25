import socket
import ssl
import threading       

def receive_messages(ssl_socket):
    while True:
        try:
            message = ssl_socket.recv(1024).decode()
            print(message)
        except:
            print("The Connection lost.")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False  
    ssl_context.verify_mode = ssl.CERT_NONE  
    secure_socket = ssl_context.wrap_socket(client_socket)
    secure_socket.connect(("127.0.0.1", 120))
    print("Connected to the secure chat server.")
    threading.Thread(target=receive_messages, args=(secure_socket,)).start()
    while True:
        try:
            message = input()
            secure_socket.send(message.encode())
        except:
            print("can not send message we have error.")
            break

if __name__ == "__main__":
    main()
