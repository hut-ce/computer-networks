import socket
def start_client(host="127.0.0.1", port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    try:
        while True:
            command = input("Enter command to execute (type 'exit' to quit): ")
            if command.lower() == "exit":
                print("Exiting...")
                break
            client_socket.send(command.encode("utf-8"))
            output = client_socket.recv(1024).decode("utf-8")
            print(f"Server Output:\n{output}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
