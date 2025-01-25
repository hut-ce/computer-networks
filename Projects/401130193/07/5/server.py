import socket
import threading


def start_server(port: int):
    """Start a server on the given port to handle client connections."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('127.0.0.1', port))
            server_socket.listen(5)
            print(f'[INFO] Server active on port {port}')

            while True:
                client_socket, client_address = server_socket.accept()
                print(f'[CONNECTION] Client {client_address} connected on port {port}')
                client_socket.close()
                print(f'[DISCONNECTED] Client {client_address} disconnected from port {port}')

    except OSError as e:
        print(f'[ERROR] Unable to bind server on port {port}: {e}')


# Define multiple ports for the server to listen on.
server_ports = [8001, 8020, 8045]

if __name__ == '__main__':
    for port in server_ports:
        threading.Thread(target=start_server, args=(port,)).start()
