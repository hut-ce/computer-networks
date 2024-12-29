import socket
import threading
import time

# الگوریتم های داده شده در صورت سوال
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def stalin_sort(arr):
    if not arr:
        return []
    sorted_list = [arr[0]]
    for i in range(1, len(arr)):
        if arr[i] >= sorted_list[-1]:
            sorted_list.append(arr[i])
    return sorted_list

def bogo_sort(arr):
    import random
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr
def client(connection, addr, algorithm):
    try:
        data = connection.recv(1024).decode()
        array = list(map(int, data.split(',')))
        print(f"[{addr}] Received array: {array}")
        start_time = time.time()
        if algorithm == "bubble":
            sorted_array = bubble_sort(array)
        elif algorithm == "stalin":
            sorted_array = stalin_sort(array)
        elif algorithm == "bogo":
            sorted_array = bogo_sort(array)
        else:
            sorted_array = []
        elapsed_time = time.time() - start_time
        connection.send(f"{sorted_array}|{elapsed_time:.4f}".encode())
        print(f"[{addr}] Sent sorted array: {sorted_array} in {elapsed_time:.4f}s")
    except Exception as e:
        connection.send(f"ERROR: {str(e)}".encode())
        print(f"[{addr}] Error: {str(e)}")
    finally:
        connection.close()
def server_program():
    host = socket.gethostbyname(socket.gethostname())
    port = 5050
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(3)
    print("waiting for connections...")
    algorithms = ["bubble", "stalin", "bogo"]
    threads = []
    for algorithm in algorithms:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=client, args=(conn, addr, algorithm))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All clients processed. Server shutting down.")
    server_socket.close()

if __name__ == "__main__":
    server_program()
