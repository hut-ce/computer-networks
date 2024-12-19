import socket

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
import random
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
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers

def handle_client(connection):
    numbers = list(map(int, connection.recv(1024).decode().split()))
    results = (
        f"Stalin Sort: {stalin_sort(numbers)}\n "
        f"Bogo Sort: {bogo_sort(numbers)}\n "
        f"Bubble Sort: {bubble_sort(numbers)}"
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
