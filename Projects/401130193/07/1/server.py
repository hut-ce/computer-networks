import socket
import threading

connected_clients = []

def broadcast_message(excluded_socket, msg):
    for conn in connected_clients:
        if conn.connection_socket != excluded_socket:
            conn.send_message(msg)

class ClientHandler:
    def __init__(self, connection_socket: socket.socket, client_address):
        self.connection_socket = connection_socket
        self.client_address = client_address

    def send_message(self, msg):
        self.connection_socket.sendall(msg)

    def handle_communication(self):
        with self.connection_socket as conn:
            while True:
                try:
                    incoming_msg = conn.recv(4096)
                    print(f"Message from client: {incoming_msg}")
                    if not incoming_msg:
                        break
                    broadcast_message(excluded_socket=conn, msg=incoming_msg)
                except ConnectionResetError:
                    break
            print(f"Client disconnected: {self.client_address}")
            connected_clients.remove(self)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('127.0.0.1', 2000))
        server.listen()
        print("Server is up and running on port 2000")

        while True:
            conn_socket, addr = server.accept()
            print(f"Connection established with: {addr}")
            client_handler = ClientHandler(conn_socket, addr)
            connected_clients.append(client_handler)
            threading.Thread(target=client_handler.handle_communication).start()

if __name__ == '__main__':
    start_server()
