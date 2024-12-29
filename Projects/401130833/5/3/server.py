import socket
import threading
import random
import time


def stalin_sort(array):
    if not array:
        return []
    sorted_list = [array[0]]
    for i in range(1, len(array)):
        if array[i] >= sorted_list[-1]:
            sorted_list.append(array[i])
    return sorted_list


def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def bogosort(array):
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    while not is_sorted(array):
        random.shuffle(array)
    return array


IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(10)

print("Server is running and waiting for connections...")

clients = []


def handle_client(connection, address):
    print(f"Client {address} connected.")
    clients.append(connection)

    try:
        while True:
            message = connection.recv(1024).decode()
            if not message:
                break

            print(f"Received array from {address}: {message}")
            try:
                array = list(map(int, message.split(",")))
            except ValueError:
                connection.send("Invalid array format. Please send integers separated by commas.".encode('utf-8'))
                continue

            # Sort the array using different sorting algorithms
            algorithms = [stalin_sort, bubble_sort, bogosort]
            sorted_arrays = {}

            for algo in algorithms:
                start_time = time.time()
                sorted_array = algo(array[:])  # Pass a copy of the array
                execution_time = time.time() - start_time
                sorted_arrays[algo.__name__] = (sorted_array, execution_time)

            # Send the sorted array (from bubble sort as an example) back to the client
            response = ",".join(map(str, sorted_arrays["bubble_sort"][0]))
            connection.send(response.encode('utf-8'))

    except (ConnectionResetError, ConnectionAbortedError):
        print(f"Connection with {address} lost.")
    finally:
        clients.remove(connection)
        connection.close()
        print(f"Client {address} disconnected.")


def start_server():
    try:
        while True:
            connection, address = server.accept()
            threading.Thread(target=handle_client, args=(connection, address)).start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.close()


if __name__ == "__main__":
    start_server()
