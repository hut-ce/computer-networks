import socket
import subprocess

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 45))
    server_socket.listen(1)
    print("waiting for connections on 127.0.0.1:45")
    connection, addr = server_socket.accept()
    print(f"{addr} connection has been started")
    try:
        while True:
            command = connection.recv(1024).decode()
            if command.lower() == "exit":
                print("Client Disconnected.")
                break
            print(f"command : {command}")
            try:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as error:
                result = error.output
            connection.send(result.encode())
    except Exception as error:
        print(f"The error {error} has been occurred")
    finally:
        connection.close()
        server_socket.close()
