import socket
import threading


def server_program(port: int):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(('127.0.0.1', port))
            server.listen(5)
            print(f'Server is listening on: localhost:{port}')

            while True:
                client_socket, address = server.accept()
                print(f'Client connected: {address} on port: {port}')
                client_socket.close()
                print(f'Client closed: {address} on port: {port}')
    
    except ConnectionResetError as e:
        print(f'Error in server on port {port}: {e}')

portes = [8010, 8023, 8049]

if __name__ == '__main__':
    for port in portes:
        threading.Thread(target=server_program, args=(port,)).start()
