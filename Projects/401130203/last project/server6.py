import socket
import threading
import time

request_counts = {}
blocked_clients = {}

MAX_REQUESTS = 10
TIME_WINDOW = 5

def handle_client(client_socket, client_address):
    global request_counts, blocked_clients

    print(f"Connection from {client_address}")

    while True:
        try:
            if client_address in blocked_clients:
                client_socket.send(b"Connection blocked due to excessive requests.\n")
                break

            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                break

            print(f"Received from {client_address}: {message}")
            current_time = time.time()
            if client_address not in request_counts:
                request_counts[client_address] = []
            request_counts[client_address].append(current_time)
            request_counts[client_address] = [
                t for t in request_counts[client_address]
                if current_time - t <= TIME_WINDOW
            ]
            if len(request_counts[client_address]) > MAX_REQUESTS:
                print(f"Blocking {client_address} due to DDOS behavior.")
                blocked_clients[client_address] = True
                client_socket.send(b"You have been blocked for sending too many requests.\n")
                break
            client_socket.send(b"Request received.\n")
        except ConnectionResetError:
            break
    client_socket.close()
    print(f"Connection with {client_address} closed.")
def start_server(host="127.0.0.1", port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
