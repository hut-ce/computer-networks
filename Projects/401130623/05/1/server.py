import socket
import random

def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr) - 1))

def bogosort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def stalin_sort(arr):
    if not arr:
        return []
    sorted_list = [arr[0]]
    for i in range(1, len(arr)):
        if arr[i] >= sorted_list[-1]:
            sorted_list.append(arr[i])
    return sorted_list

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def handle_client(conn):
    data = conn.recv(1024)
    numbers = eval(data.decode('utf-8'))

    sorted_numbers = [bogosort(numbers.copy()), stalin_sort(numbers.copy()), bubble_sort(numbers.copy())]
    
    for sorted_arr in sorted_numbers:
        conn.sendall(str(sorted_arr).encode('utf-8'))

server_address = ('localhost', 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)
s.listen(1)

print('waiting for client connection')
while True:
    conn, addr = s.accept()
    try:
        print('client connected:', addr)
        handle_client(conn)
    finally:
        conn.close()