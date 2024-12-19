import socket
from multiprocessing import Process


def client_program(arr: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('127.0.0.1', 8080))
        try:
            client.send(arr.encode())
            print(f'SNET: {arr}')

            response = client.recv(1024).decode()
            print(f'RECEIVED: {response}')
        except Exception as e:
            print(f'ERROR: {e}')


if __name__ == '__main__':
    value = []
    for i in range(3):
        value.append(input(f'Enter array {i + 1}: '))

    process1 = Process(target=client_program, args=(value[0],))
    process2 = Process(target=client_program, args=(value[1],))
    process3 = Process(target=client_program, args=(value[2],))

    process1.start()
    process2.start()
    process3.start()

