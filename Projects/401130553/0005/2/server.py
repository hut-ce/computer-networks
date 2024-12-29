import socket
from multiprocessing import Process


def client_handler(client_socket, address):
    print(f'NEW CONNECTION: {address}')
    try:
        data = client_socket.recv(1024).decode()
        arr = list(map(int, data.split()))
        print(f'RECEIVED: {arr} from {address}')
        arr.sort()
        client_socket.send(','.join(map(str, arr)).encode())
        print(f'SENT: {arr} to {address}')
    except Exception as e:
        print(f'ERROR: error handling client {address}: {e}')
    finally:
        print(f'DISCONNECTED: {address}\n')


def server_program():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('127.0.0.1', 8080))
        server.listen(3)
        print('Server listening on localhost:8080...\n')
        while True:
            client, address = server.accept()
            with client:
                # print(f'ACCEPTED: connection from {address}')
                process = Process(target=client_handler, args=(client, address))
                process.start()


if __name__ == '__main__':
    server_program()
