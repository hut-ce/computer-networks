import socket
import threading
import logging

HOST = '127.0.0.1'
PORT = 12345

# log
logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

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
        for j in range(n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return numbers

def handle_client(connection, address):
    logging.info(f"Connected by {address}")
    try:
        data = connection.recv(1024).decode()
        if not data:
            raise ValueError("Received empty data")
        numbers = list(map(int, data.split()))
        stalin_sorted = stalin_sort(numbers)
        bogo_sorted = bogo_sort(numbers)
        bubble_sorted = bubble_sort(numbers)

        results = (
            f"Stalin Sort: {stalin_sorted} "
            f"Bogo Sort: {bogo_sorted} "
            f"Bubble Sort: {bubble_sorted}"
        )
        connection.send(results.encode())
        logging.info(f"Sent results to {address}")
    except Exception as e:
        logging.error(f"Error handling client {address}: {e}")
        connection.send(f"Error: {e}".encode())
    finally:
        connection.close()

# server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(3)

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
