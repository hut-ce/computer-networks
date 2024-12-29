import socket
import pickle
import random
import time


# To check if array is sorted or not
def is_sorted(a):
    n = len(a)
    for i in range(0, n - 1):
        if a[i] > a[i + 1]:
            return False
    return True


# To generate permutation of the array
def shuffle(a):
    n = len(a)
    for i in range(0, n):
        r = random.randint(0, n - 1)
        a[i], a[r] = a[r], a[i]


def bogo_sort(a):
    while not is_sorted(a):
        shuffle(a)


def so2_program():
    try:
        with socket.socket() as so2:
            so2.bind(('127.0.0.1', 8002))
            so2.listen(1)
            print('SO2 waiting for a connection')
            server, server_address = so2.accept()
            print('SO2 connected to server')
            start_time = time.time()
            data = server.recv(1024)
            arr = pickle.loads(data)
            bogo_sort(arr)
            end_time = time.time()
            print(f'SO2 sorted array: {arr}')
            server.send(pickle.dumps({'sorted': arr, 'name': 'Bogo Sort', 'time': f'{end_time - start_time:.4}'}))
            server.close()
    except Exception as e:
        print(f'SO2 error: {e}')


if __name__ == '__main__':
    so2_program()
