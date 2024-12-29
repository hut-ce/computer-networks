import socket
import time
import random

HOST = '127.0.0.1'
PORT = 12345

# stalin
def stalin_sort(numbers):
    sorted_list = [numbers[0]]
    for number in numbers[1:]:
        if number >= sorted_list[-1]:
            sorted_list.append(number)
    return sorted_list

# bogo
def bogo_sort(numbers):
    while not all(numbers[i] <= numbers[i + 1] for i in range(len(numbers) - 1)):
        random.shuffle(numbers)
    return numbers

# bubble
def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j], numbers[j+1]
    return numbers

def handle_client(connection):
    numbers = list(map(int, connection.recv(1024).decode().split()))

    # time
    start_time = time.time()
    stalin_sorted = stalin_sort(numbers)
    stalin_time = time.time() - start_time

    start_time = time.time()
    bogo_sorted = bogo_sort(numbers)
    bogo_time = time.time() - start_time

    start_time = time.time()
    bubble_sorted = bubble_sort(numbers)
    bubble_time = time.time() - start_time

    # fastest
    times = {"Stalin Sort": stalin_time, "Bogo Sort": bogo_time, "Bubble Sort": bubble_time}
    fastest = min(times, key=times.get)

    results = (
        f"Stalin Sort: {stalin_sorted} time: {stalin_time:.6f}s\n "
        f"Bogo Sort: {bogo_sorted} time: {bogo_time:.6f}s\n "
        f"Bubble Sort: {bubble_sorted} time: {bubble_time:.6f}s\n "
        f"fastest algorithm: {fastest}"
    )
    connection.send(results.encode())
    connection.close()

# server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

while True:
    conn, addr = server.accept()
    handle_client(conn)
