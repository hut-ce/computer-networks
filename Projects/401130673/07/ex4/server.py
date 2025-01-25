import socket
import threading

data_store = {}

def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            command, key, value = request.split(" ")
            if command == "SET":
                data_store[key] = value
                response = f"Key {key} set to {value}"
            elif command == "GET":
                response = data_store.get(key, "Key not found")
            else:
                response = "Invalid command"
            client_socket.send(response.encode('utf-8'))
    except ConnectionResetError:
        client_socket.close()

def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 5055))
        server.listen(5)
        print("Server started on port 5055...")
        while True:
            client_socket, addr = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except ConnectionResetError:
        server.close()

if __name__ == "__main__":
    start_server()
