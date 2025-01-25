import socket
import ssl
import threading
HOST = '127.0.0.1'
PORT = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
print(f"Secure chat server started on {HOST}:{PORT}")
clients = []
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    clients.append(client_socket)
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{client_address}: {message}")
            broadcast(message, client_socket)
    except:
        pass
    finally:
        print(f"Connection closed for {client_address}")
        clients.remove(client_socket)
        client_socket.close()
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass
while True:
    client_socket, client_address = server_socket.accept()
    secure_socket = context.wrap_socket(client_socket, server_side=True)
    threading.Thread(target=handle_client, args=(secure_socket, client_address)).start()
