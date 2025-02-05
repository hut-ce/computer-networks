import socket
import threading
import time
import random

# Sorting Algorithms
def stalin_sort(arr):
    if not arr:
        return []
    sorted_list = [arr[0]]
    for i in range(1, len(arr)):
        if arr[i] >= sorted_list[-1]:
            sorted_list.append(arr[i])
    return sorted_list

def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

def bogo_sort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Function to handle each client
def handle_client(client_socket, addr):
    try:
        print(f"Connected to {addr}")
        # Receive array from client
        data = client_socket.recv(1024).decode()
        array = list(map(int, data.split(',')))  # Convert received string to a list of integers
        print(f"Received array from {addr}: {array}")

        # Initialize sorting algorithms
        algorithms = {
            "Stalin Sort": stalin_sort,
            "Bogo Sort": bogo_sort,
            "Bubble Sort": bubble_sort,
        }

        results = []
        threads = []

        # Run sorting algorithms in parallel
        def sort_and_measure(algo_name, algo_func):
            start_time = time.time()
            sorted_array = algo_func(array.copy())
            duration = time.time() - start_time
            results.append(f"{algo_name}:{','.join(map(str, sorted_array))}:{duration:.4f}")

        for algo_name, algo_func in algorithms.items():
            thread = threading.Thread(target=sort_and_measure, args=(algo_name, algo_func))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Send results back to the client as a single string
        response = ";".join(results)
        client_socket.send(response.encode())
        print(f"Results sent to {addr}")

    except Exception as e:
        error_message = f"Error: {e}"
        client_socket.send(error_message.encode())
        print(f"Error with {addr}: {e}")

    finally:
        client_socket.close()
        print(f"Connection to {addr} closed.")

# Main server function
def main():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server is running on {host}:{port}")

        while True:
            try:
                client_socket, addr = server_socket.accept()
                threading.Thread(target=handle_client, args=(client_socket, addr)).start()
            except Exception as e:
                print(f"Server error: {e}")

if __name__ == "__main__":
    main()
