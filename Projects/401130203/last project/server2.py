import socket
import os
def start_server(host="127.0.0.1", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}. Waiting for connections...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        try:
            while True:
                command = client_socket.recv(1024).decode("utf-8")
                if not command or command.lower() == "exit":
                    print("Connection closed by the client.")
                    break

                print(f"Received command: {command}")
                try:
                    output = os.popen(command).read()
                    if not output.strip():
                        output = "Command executed successfully with no output."
                except Exception as e:
                    output = f"Error executing command: {str(e)}"
                client_socket.send(output.encode("utf-8"))
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()
