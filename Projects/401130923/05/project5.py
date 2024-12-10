import socket
import threading
import random
import time

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def bogo_sort(arr):
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def stalin_sort(arr):
    result = [arr[0]]
    for num in arr[1:]:
        if num >= result[-1]:
            result.append(num)
    return result

class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = []

    def handle_client(self, client_socket, address):
        print(f"Connected to {address}")
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            print(f"[RECEIVED] Array from client: {data}")
            arr = list(map(int, data.split(',')))

            threads = []
            results = []
            def send_to_so(sort_function, index):
                sorted_array = sort_function(arr[:])
                results.append((index, sorted_array))

            for i, sort_function in enumerate([bubble_sort, bogo_sort, stalin_sort]):
                thread = threading.Thread(target=send_to_so, args=(sort_function, i))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            results.sort(key=lambda x: x[0])
            sorted_arrays = [res[1] for res in results]
            response = "|".join(["Sorted by SO" + str(i + 1) + ": " + str(arr) for i, arr in enumerate(sorted_arrays)])
            client_socket.send(response.encode('utf-8'))
        client_socket.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port

    def send_array(self, arr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            array_str = ",".join(map(str, arr))
            client_socket.send(array_str.encode('utf-8'))
            result = client_socket.recv(1024).decode('utf-8')
            print(f"[Result] {result}")

if __name__ == "__main__":
    server = Server()
    threading.Thread(target=server.start).start()

    time.sleep(1)  # صبر برای آماده شدن سرور
    client = Client()
    input_array = list(map(int, input("Enter array elements separated by comma: ").split(',')))
    client.send_array(input_array)
