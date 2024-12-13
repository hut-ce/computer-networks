import socket
import threading
import time
import random


def stalin_sort(array):
    if not array:
        return []
    sorted_list = [array[0]]
    for i in range(1, len(array)):
        if array[i] >= sorted_list[-1]:
            sorted_list.append(array[i])
        return sorted_list


def is_sorted(arr):
    """Helper function to check if the list is sorted."""
    return all(arr[i] <= arr[i+1] for i in range(len(arr) - 1))


def bogosort(arr):
    """Shuffles the array until it is sorted."""
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr


def bubble_sort(arr):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

server.listen(10)


print("Server is Running and is waiting for connections...")

clients = []


def handle_clients(connection, address):
    print(f"{address} is connected to the server!")
    while True:
        try:
            fastest_time = 0
            fastest_algorithm = ""
            message = connection.recv(1024).decode()

            if not message:
                break
            print(f"{address} gave this array {message}\n")

            array = message.split(",")
            start_time = time.time()
            print(f"stalin sort on {array} gave {stalin_sort(array)}")
            end_time = time.time()
            exe_time = end_time - start_time
            fastest_time = end_time
            fastest_algorithm = "stalin sort"
            print(f"and it took {exe_time} seconds\n")

            start_time = time.time()
            print(f"bogo sort on {array} gave {bogosort(array)}")
            end_time = time.time()
            exe_time = end_time - start_time
            if exe_time < fastest_time:
                fastest_time = exe_time
                fastest_algorithm = "bogo sort"
            print(f"and it took {exe_time} seconds\n")

            start_time = time.time()
            print(f"bubble sort on {array} gave {bubble_sort(array)}")
            end_time = time.time()
            exe_time = end_time - start_time
            if exe_time < fastest_time:
                fastest_time = exe_time
                fastest_algorithm = "bubble sort"
            print(f"and it took {exe_time:.10f} seconds\n")

            print(f"the fastest time was: {fastest_time} achieved using: {fastest_algorithm}")

        except KeyboardInterrupt:
            print(f"Connection with {address} is closed")
            break
        except ConnectionResetError:
            print(f"Connection with {address} was forcibly closed")
            break

    clients.remove(connection)
    connection.close()
    print(f"{address} has been disconnected")


try:
    while True:
        connection, address = server.accept()
        clients.append(connection)
        thread = threading.Thread(target=handle_clients, args=(connection, address))
        thread.start()

except KeyboardInterrupt:
    print("Shutting down...")
    server.close()



