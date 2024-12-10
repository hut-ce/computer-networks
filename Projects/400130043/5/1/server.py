import socket
import threading
import random

def sort_bubble(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def handle_client(client_socket):
    data = client_socket.recv(1024).decode()
    print(f"Received array from client: {data}")
    arr = list(map(int, data.split()))

    results = []
    threads = []
    algorithms = [sort_bubble]

    for algo in algorithms:
        thread = threading.Thread(target=lambda q, arg1: q.append(algo(arg1)), args=(results, arr.copy()))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    result_str = ', '.join(map(str, results))
    client_socket.send(result_str.encode())
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
