import socket
import ssl
import threading   

clients = []
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:  
            try:
                client.send(message)
            except:
                clients.remove(client)

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

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.0", 120))
    server_socket.listen(5)
    print("Server is listening on 127.0.0.0:120")

    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="serv.crt", keyfile="serv.key")
    secure_socket = ssl_context.wrap_socket(server_socket, server_side=True)

    while True:
        client_socket, client_address = secure_socket.accept()
        print(f"{client_address} has connected securly.")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
