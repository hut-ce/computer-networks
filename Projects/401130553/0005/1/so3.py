import socket
import pickle
import time


def bubble_sort(arr):
    # Outer loop to iterate through the list n times
    for n in range(len(arr) - 1, 0, -1):

        # Initialize swapped to track if any swaps occur
        swapped = False

        # Inner loop to compare adjacent elements
        for i in range(n):
            if arr[i] > arr[i + 1]:
                # Swap elements if they are in the wrong order
                arr[i], arr[i + 1] = arr[i + 1], arr[i]

                # Mark that a swap has occurred
                swapped = True

        # If no swaps occurred, the list is already sorted
        if not swapped:
            break


def so3_program():
    try:
        with socket.socket() as so3:
            so3.bind(('127.0.0.1', 8003))
            so3.listen(1)
            print('SO3 waiting for a connection')
            server, server_address = so3.accept()
            print('SO3 connected to server')
            start_time = time.time()
            data = server.recv(1024)
            arr = pickle.loads(data)
            bubble_sort(arr)
            end_time = time.time()
            print(f'SO3 sorted array: {arr}')
            server.send(pickle.dumps({'sorted': arr, 'name': 'Bubble Sort', 'time': f'{end_time - start_time:.4}'}))
            server.close()
    except Exception as e:
        print(f'SO2 error: {e}')


if __name__ == '__main__':
    so3_program()
