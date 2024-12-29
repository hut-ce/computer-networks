import socket
import threading
import logging
import random
import time

logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def stalin_sort(arr):
    if not arr:
        return []
    result = [arr[0]]
    for num in arr[1:]:
        if num >= result[-1]:
            result.append(num)
    return result

def bogo_sort(arr):
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
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

sorting_algorithms = {
    "Stalin": stalin_sort,
    "Bogo": bogo_sort,
    "Bubble": bubble_sort
}

def handle_client(client_socket, addr, algo_name, arr):
    try:
        logging.info(f"{algo_name} started sorting for client {addr}.")
        start_time = time.time()
        sorted_arr = sorting_algorithms[algo_name](arr)
        elapsed_time = time.time() - start_time
        client_socket.send(f"{algo_name}: Sorted array: {sorted_arr}, Time: {elapsed_time:.4f}s".encode())
        logging.info(f"{algo_name} finished sorting: {sorted_arr}, Time: {elapsed_time:.4f}s.")
    except Exception as e:
        logging.error(f"Error in {algo_name} for client {addr}: {e}")
        client_socket.send(f"Error: {e}".encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(4)
    logging.info("Server started. Waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        logging.info(f"Client connected: {addr}")
        try:
            data = client_socket.recv(1024).decode()
            if data.startswith("Array:"):
                arr = list(map(int, data.replace("Array:", "").split()))
                logging.info(f"Received array from client {addr}: {arr}")

                threads = []
                for algo_name in sorting_algorithms:
                    t = threading.Thread(target=handle_client, args=(client_socket, addr, algo_name, arr))
                    threads.append(t)
                    t.start()

                for t in threads:
                    t.join()
            else:
                logging.warning(f"Invalid data received from {addr}: {data}")
        except Exception as e:
            logging.error(f"Error handling client {addr}: {e}")
            client_socket.send(f"Server error: {e}".encode())
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
