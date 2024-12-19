import socket
import threading
import random
import time  

# Algorithm Implementations
def stalin_sort(arr):
    if not arr:
        return []
    sorted_list = [arr[0]]
    for i in range(1, len(arr)):
        if arr[i] >= sorted_list[-1]:
            sorted_list.append(arr[i])
    return sorted_list

def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr) - 1))

def bogosort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Server Code
def handle_sorting(client_socket, algorithm):
    data = client_socket.recv(1024).decode()
    array = list(map(int, data.split(',')))
    
    
    start_time = time.time()

    if algorithm == "stalin":
        result = stalin_sort(array)
    elif algorithm == "bogo":
        result = bogosort(array)
    elif algorithm == "bubble":
        result = bubble_sort(array)
    else:
        result = []

    end_time = time.time()
    elapsed_time = end_time - start_time  

    
    result_str = ','.join(map(str, result)) + f" (Time: {elapsed_time:.4f} seconds)"
    client_socket.send(result_str.encode())
    client_socket.close()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)

    print("Server is listening...")

    client_socket, addr = server_socket.accept()
    print(f"Connected to client at {addr}")

    data = client_socket.recv(1024).decode()
    print(f"Received array: {data}")
    
    # Forwarding data to SO clients
    algorithms = ["stalin", "bogo", "bubble"]
    results = []

    def forward_to_so(algorithm):
        so_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so_socket.connect(("localhost", 12346))
        so_socket.send(data.encode())
        sorted_data = so_socket.recv(1024).decode()
        results.append((algorithm, sorted_data))
        so_socket.close()

    threads = []
    for algo in algorithms:
        thread = threading.Thread(target=forward_to_so, args=(algo,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    
    fastest_algo = min(results, key=lambda x: float(x[1].split(" (Time: ")[1].split(" ")[0]))

    
    for algo, sorted_result in results:
        client_socket.send(f"{algo}: {sorted_result}\n".encode())
    
    
    client_socket.send(f"Fastest algorithm: {fastest_algo[0]}\n".encode())

    client_socket.close()
    server_socket.close()

# Client Code for Main Client
def main_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 12345))

    array = input("Enter an array of numbers separated by commas: ")
    client_socket.send(array.encode())

    print("Waiting for sorted results...")
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(data)

    client_socket.close()

# Client Code for SOs
def so_client(algorithm):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12346))
    server_socket.listen(5)

    print(f"SO Client ({algorithm}) is ready...")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to server at {addr}")

        data = client_socket.recv(1024).decode()
        print(f"Received data for sorting ({algorithm}): {data}")
        array = list(map(int, data.split(',')))

        if algorithm == "stalin":
            result = stalin_sort(array)
        elif algorithm == "bogo":
            result = bogosort(array)
        elif algorithm == "bubble":
            result = bubble_sort(array)
        else:
            result = []

        client_socket.send(','.join(map(str, result)).encode())
        client_socket.close()

if __name__ == "__main__":
    # Uncomment the function you want to run
    # server()
    # main_client()
    # so_client("stalin")
    # so_client("bogo")
    # so_client("bubble")
