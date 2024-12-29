import socket
import threading

clients = {}  
addresses = {}  

def broadcast(message, exclude_client=None):
    for client, (sock, _) in clients.items():
        if client != exclude_client:
            sock.send(message.encode('utf-8'))


# Handle Client Communication
def handle_client(client_socket, client_address):
    try:
        name = client_socket.recv(1024).decode()
        if not name:
            client_socket.close()
            return

        welcome_message = f"{name} has joined the chat!"
        broadcast(welcome_message)
        print(welcome_message)

        clients[name] = (client_socket, client_address)

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message.startswith("private"):
                _, recipient, encrypted_message = message.split(" ", 2)
                if recipient in clients:
                    recipient_sock = clients[recipient][0]
                    recipient_sock.send(f"Private from {name}: {encrypted_message}".encode('utf-8'))
                else:
                    client_socket.send(f"{recipient} is not connected.".encode('utf-8'))

            elif message.startswith("block"):
                _, block_name = message.split(" ", 1)
                if block_name in clients:
                    client_socket.send(f"You have blocked {block_name}.".encode('utf-8'))
                else:
                    client_socket.send(f"{block_name} is not connected.".encode('utf-8'))

            elif message.startswith("login"):
                _, username, password = message.split(" ", 2)
                client_socket.send(f"Welcome back, {username}!".encode('utf-8'))

            elif message == "quit!!!":
                break

            else:
                formatted_message = f"{name}: {message}"
                broadcast(formatted_message, exclude_client=name)
                print(formatted_message)

    except (ConnectionResetError, ConnectionAbortedError):
        print(f"Connection with {client_address} lost.")

    finally:
        if name in clients:
            del clients[name]
            broadcast(f"{name} has left the chat.")
            print(f"{name} disconnected.")
        client_socket.close()


# Start the Server
def start_server():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Server started on {HOST}:{PORT}. Waiting for connections...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection established with {client_address}.")

        # Start a new thread for each client
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()


if __name__ == "__main__":
    start_server()
