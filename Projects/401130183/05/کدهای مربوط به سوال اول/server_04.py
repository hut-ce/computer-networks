import socket
import threading
import time
import random
import logging

logging.basicConfig(filename='server_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

array_from_client = None
connected_clients = []
sorting_times = {}

def stalin_sort(arr):
    try:
        result = [arr[0]]
        for num in arr[1:]:
            if num >= result[-1]:
                result.append(num)
        return result
    except Exception as e:
        logging.error(f"Error in Stalin Sort: {str(e)}")
        return f"Error in Stalin Sort: {str(e)}"

def bogo_sort(arr):
    try:
        def is_sorted(lst):
            return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

        attempts = 0
        while not is_sorted(arr):
            random.shuffle(arr)
            attempts += 1
            if attempts > 1000:  
                logging.error("Too many attempts in Bogo Sort")
                return "Error: Too many attempts in Bogo Sort"
        return arr
    except Exception as e:
        logging.error(f"Error in Bogo Sort: {str(e)}")
        return f"Error in Bogo Sort: {str(e)}"

def bubble_sort(arr):
    try:
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    except Exception as e:
        logging.error(f"Error in Bubble Sort: {str(e)}")
        return f"Error in Bubble Sort: {str(e)}"

def handle_client(client_socket, client_address, client_id):
    global array_from_client, sorting_times
    connected_clients.append(client_socket)
    logging.info(f"Client connected: {client_address}")

    try:
        if array_from_client is None:
            data = client_socket.recv(1024).decode('utf-8')
            array_from_client = list(map(int, data.split(',')))
            logging.info(f"Received array from client {client_address}: {array_from_client}")
            client_socket.send("Array received successfully!".encode('utf-8'))
        else:
            algorithms = [stalin_sort, bogo_sort, bubble_sort]
            algorithm_names = ["Stalin Sort", "Bogo Sort", "Bubble Sort"]

            if client_id - 1 <= len(algorithms):
                algorithm = algorithms[client_id - 2]
                algorithm_name = algorithm_names[client_id - 2]

                start_time = time.time()
                sorted_array = algorithm(array_from_client.copy())
                end_time = time.time()
                elapsed_time = end_time - start_time
                sorting_times[algorithm_name] = elapsed_time

                if isinstance(sorted_array, str) and "Error" in sorted_array:
                    message = f"Error during sorting: {sorted_array}"
                else:
                    message = (
                        f"Sorted Array: {sorted_array}\n"
                        f"Algorithm: {algorithm_name}\n"
                        f"Execution Time: {elapsed_time:.6f} seconds"
                    )
                client_socket.send(message.encode('utf-8'))
            else:
                client_socket.send("No sorting task assigned.".encode('utf-8'))

        if len(sorting_times) == 3:
            fastest_algorithm = min(sorting_times, key=sorting_times.get)
            logging.info(f"Fastest Algorithm: {fastest_algorithm}")
            for client in connected_clients:
                try:
                    client.send(f"Fastest Algorithm: {fastest_algorithm}".encode('utf-8'))
                except Exception as e:
                    logging.error(f"Error sending message to client: {str(e)}")

    except Exception as e:
        logging.error(f"Error handling client {client_address}: {str(e)}")
        client_socket.send(f"An error occurred: {str(e)}".encode('utf-8'))
    finally:
        client_socket.close()

def server_program():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 5555))
        server_socket.listen(5)
        logging.info("Server is listening on port 5555...")

        client_id = 0
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                client_id += 1
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_id))
                client_thread.start()
            except Exception as e:
                logging.error(f"Error accepting connection: {str(e)}")
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    server_program()