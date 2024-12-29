import socket
import threading
import time
import random


def stalin_sort(array):
    if not array:
        return []
    result = [array[0]]
    for num in array[1:]:
        if num >= result[-1]:
            result.append(num)
    return result


def bogo_sort(array):
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    while not is_sorted(array):
        random.shuffle(array)
    return array


def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array
def handle_client(client_socket, address, so_clients):
    try:
        print(f"[INFO] Connection established with {address}")


        array = client_socket.recv(1024).decode()
        array = list(map(int, array.split()))
        print(f"[RECEIVED] Array from main client: {array}")


        so_results = {}
        threads = []

        def sort_and_receive(so_client, algo_name):
            so_client.send(" ".join(map(str, array)).encode())
            start_time = time.time()
            sorted_array = so_client.recv(1024).decode()
            elapsed_time = time.time() - start_time
            sorted_array = list(map(int, sorted_array.split()))
            so_results[algo_name] = (sorted_array, elapsed_time)

        for algo_name, so_client in so_clients.items():
            thread = threading.Thread(target=sort_and_receive, args=(so_client, algo_name))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


        results_to_send = "\n".join(
            f"{algo}: {result[0]} (time: {result[1]:.4f}s)"
            for algo, result in so_results.items()
        )
        client_socket.send(results_to_send.encode())


        fastest_algo = min(so_results, key=lambda k: so_results[k][1])
        fastest_message = f"Fastest algorithm: {fastest_algo} with time {so_results[fastest_algo][1]:.4f}s"
        client_socket.send(fastest_message.encode())

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()


def so_worker(algorithm):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    port = server.getsockname()[1]
    print(f"[INFO] SO ({algorithm.__name__}) listening on port {port}")
    server.listen(1)

    while True:
        client_socket, address = server.accept()
        try:
            array = client_socket.recv(1024).decode()
            array = list(map(int, array.split()))
            sorted_array = algorithm(array)
            client_socket.send(" ".join(map(str, sorted_array)).encode())
        except Exception as e:
            print(f"[ERROR in {algorithm.__name__}] {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":

    so_algorithms = [stalin_sort, bogo_sort, bubble_sort]
    so_clients = {}

    for algo in so_algorithms:
        thread = threading.Thread(target=so_worker, args=(algo,))
        thread.daemon = True
        thread.start()

    time.sleep(1)


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen(1)
    print("[INFO] Server listening on port 5555")

    client_socket, address = server.accept()
    handle_client(client_socket, address, so_clients)
