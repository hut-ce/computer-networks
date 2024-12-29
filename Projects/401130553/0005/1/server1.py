import socket
import multiprocessing
import pickle
from time import sleep


def server_processor(so_socket, arr):
    so_socket.send(pickle.dumps(arr))
    response = so_socket.recv(1024)
    return pickle.loads(response)


def server_program():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(('localhost', 8090))
            server.listen(5)

            while True:
                print('Waiting for connection on localhost:8090...')
                try:
                    client, client_address = server.accept()
                    with client:
                        print(f'Client connect by {client_address}')
                        data = client.recv(1024)
                        arr = pickle.loads(data)
                        print(f'Received array from client: {arr}')

                        so1_socket = socket.socket()
                        so1_socket.connect(('localhost', 8001))
                        so2_socket = socket.socket()
                        so2_socket.connect(('localhost', 8002))
                        so3_socket = socket.socket()
                        so3_socket.connect(('localhost', 8003))

                        with multiprocessing.Pool(3) as pool:
                            results = pool.starmap(server_processor, [
                                (so1_socket, arr),
                                (so2_socket, arr),
                                (so3_socket, arr)
                            ])
                        for result in results:
                            sleep(0.0000001)
                            client.send(pickle.dumps(result))
                except Exception as e:
                    print(f'Error during communication with client: {e}')

    except Exception as e:
        print(f'Error server disconnected: {e}')


if __name__ == '__main__':
    server_program()
