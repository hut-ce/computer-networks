import socket
import ssl
import threading


CERT = "server.crt"  
KEY = "server.key"   

clients = []


def broadcast(message, sender_socket=None):

    for client in clients:
        if client != sender_socket:  
            try:
                client.send(message)
            except:
                clients.remove(client)


def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)
    print("[SERVER] Server is listening on port 12345...")

    
    ssl_contx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_contx.load_cert_chain(certfile=CERT, keyfile=KEY)
    secure_socket = ssl_contx.wrap_socket(server_socket, server_side=True)

    while True:
        client_socket, client_address = secure_socket.accept()
        print(f"[SECURE CONNECTION] {client_address} has connected.")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"[{address}] {message.decode()}")
            broadcast(message, sender_socket=client_socket)
        except:
            break

    print(f"[DISCONNECT] {address} disconnected.")
    clients.remove(client_socket)
    client_socket.close()


if __name__ == "__main__":
    start_server()
