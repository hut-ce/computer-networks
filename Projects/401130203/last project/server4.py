import socket
import threading
data_store = {}

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                break

            command = message.split()
            response = ""

            if command[0] == "SET" and len(command) == 3:
                key, value = command[1], command[2]
                data_store[key] = value
                response = f"Key '{key}' set successfully."

            elif command[0] == "GET" and len(command) == 2:
                key = command[1]
                response = data_store.get(key, f"Key '{key}' not found.")

            elif command[0] == "DELETE" and len(command) == 2:
                key = command[1]
                if key in data_store:
                    del data_store[key]
                    response = f"Key '{key}' deleted successfully."
                else:
                    response = f"Key '{key}' not found."

            elif command[0] == "EXIT":
                response = "Goodbye!"
                client_socket.send(response.encode('utf-8'))
                break

            else:
                response = "Invalid command. Use SET, GET, DELETE, or EXIT."

            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            client_socket.send(f"Error: {e}".encode('utf-8'))

    client_socket.close()

def start_server(host="127.0.0.1", port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
