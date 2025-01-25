import socket
import ssl
import threading

HOST = '0.0.0.0'  
PORT = 12345
CERTFILE = 'server.crt' 
KEYFILE = 'server.key'    

clients = []

def handle_client(client_socket, addr):
    """مدیریت ارتباط با کلاینت"""
    print(f"new conncted {addr}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            broadcast(message, client_socket)
        except Exception as e:
            print(f"error: {e}")
            break

    print(f" {addr} disconnect.")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    """ارسال پیام به همه کلاینت‌ها به جز فرستنده"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"error in send msg: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"server {HOST}:{PORT} listening...")

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    while True:
        client_socket, addr = server_socket.accept()
        secure_socket = ssl_context.wrap_socket(client_socket, server_side=True)
        client_handler = threading.Thread(target=handle_client, args=(secure_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
