import socket
import pickle
import time


def variation_stalin_sort(arr):
    j = 0
    while True:
        moved = 0
        for i in range(len(arr) - 1 - j):
            if arr[i] > arr[i + 1]:
                arr.insert(moved, arr.pop(i + 1))
                moved += 1
        j += 1
        if moved == 0:
            break
    return arr


def stalin_sort(arr):
    if not arr:
        return []

    result = [arr[0]]
    for num in arr[1:]:
        if num >= result[-1]:
            result.append(num)
    return result


def so1_program():
    try:
        with socket.socket() as so1:
            so1.bind(('127.0.0.1', 8001))
            so1.listen(1)
            print('SO1 waiting for a connection')
            server, server_address = so1.accept()
            print('SO1 connected to server')
            start_time = time.time()
            data = server.recv(1024)
            arr = pickle.loads(data)
            sorted_arr = stalin_sort(arr)
            end_time = time.time()
            print(f'SO1 sorted array: {sorted_arr}')
            server.send(pickle.dumps({'sorted': sorted_arr, 'name': 'Stalin Sort', 'time': f'{end_time - start_time:.4}'}))
            server.close()
    except Exception as e:
        print(f'SO1 error: {e}')


if __name__ == '__main__':
    so1_program()
