import socket
import subprocess
from threading import Thread
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 9999))
    server_socket.listen(1)
    print("Server is running and waiting for connections...")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    while True:
        
        command = conn.recv(1024).decode()
        if command.lower() == "exit":
            print("Client disconnected.")
            break

        print(f"Executing command: {command}")
        try:
            
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output

        
        conn.send(result.encode())

    conn.close()
    server_socket.close()