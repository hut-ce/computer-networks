import pickle
import socket
import subprocess
from threading import Thread


def handle_client_commands(client_socket: 'socket.socket'):
    while True:
        received_data = client_socket.recv(1024)
        if received_data:
            command = pickle.loads(received_data)
            if command == 'exit':
                client_socket.close()
                break

            try:
                result = subprocess.check_output(command, shell=True, text=True)
                if not result.strip():
                    result = "No output or invalid command!"
            except subprocess.CalledProcessError:
                result = "Invalid command or execution error!"
            client_socket.send(pickle.dumps(result))


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 1234))
    server_socket.listen(5)
    print("Server is ready and listening on 127.0.0.1:1234")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New client connected from: {client_address}")
        client_thread = Thread(target=handle_client_commands, args=(client_socket,))
        client_thread.start()


if __name__ == '__main__':
    start_server()
