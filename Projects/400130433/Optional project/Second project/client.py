import socket
import subprocess
from threading import Thread
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 9999))
    print("Connected to the server.")

    while True:
       
        command = input("Enter command to execute on server (or 'exit' to quit): ")
        client_socket.send(command.encode())
        if command.lower() == "exit":
            print("Disconnecting from server.")
            break

        
        result = client_socket.recv(4096).decode()
        print(f"Result:\n{result}")

    client_socket.close()

if __name__ == "__main__":
    choice = input("Run as (server/client): ").strip().lower()
    if choice == "server":
        start_server()
    elif choice == "client":
        start_client()
    else:
        print("Invalid choice. Please select 'server' or 'client'.")
