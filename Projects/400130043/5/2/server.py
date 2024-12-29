import socket
import threading
import random
import time


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
    times = []
    
    threads = []
    algorithms = [sort_stalin, sort_bogo, sort_bubble]
    
    for algo in algorithms:
        start_time = time.time()
        
        thread = threading.Thread(target=lambda q, arg1, t: (q.append(algo(arg1)), t.append(time.time() - start_time)), args=(results, arr.copy(), times))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    fastest_index = times.index(min(times))
    fastest_algorithm = algorithms[fastest_index].name

    result_str = ', '.join(map(str, results))
    response = f"Sorted results: {result_str}\nFastest algorithm: {fastest_algorithm} with time: {times[fastest_index]:.6f} seconds"
    client_socket.send(response.encode())
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
