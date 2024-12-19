import socket
import pickle


def client_program(arr: list):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(('127.0.0.1', 8090))
            print('Client connected to server')

            client.send(pickle.dumps(arr))
            print(f'send: {arr}')

            for i in range(3):
                try:
                    data = client.recv(1024)
                    sorted_arr = pickle.loads(data)
                    print(f'{sorted_arr["name"]}: {sorted_arr["sorted"]} - {sorted_arr["time"]}s')
                except Exception as e:
                    print(f'Error receiving data: {e}')

    except Exception as e:
        print(f'Client disconnected: {e}')


if __name__ == '__main__':
    value = list(map(int, input('Enter array:').split()))
    client_program(value)

