import socket
import threading

class Server:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(3)
            print(f"Server started at {self.host}:{self.port}")
        except PermissionError as e:
            print(f"PermissionError: {e}. Try running the script as Administrator or change the port.")
            exit()

    def handle_client(self, client_socket, address):
        print(f"Client connected from {address}")
        try:
            data = client_socket.recv(1024).decode()
            array = list(map(int, data.split(',')))
            print(f"Received array from {address}: {array}")
            sorted_array = sorted(array)
            print(f"Sorted array for {address}: {sorted_array}")
            client_socket.send(','.join(map(str, sorted_array)).encode())
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection closed for {address}")

    def run(self):
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

class Client:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_array(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")

            array = input("Enter a list of numbers separated by commas: ").strip()
            self.client_socket.send(array.encode())
            data = self.client_socket.recv(1024).decode()
            sorted_array = list(map(int, data.split(',')))
            print(f"Sorted array from server: {sorted_array}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    server = Server()
    threading.Thread(target=server.run, daemon=True).start()
    for _ in range(3):
        client = Client()
        threading.Thread(target=client.send_array).start()
