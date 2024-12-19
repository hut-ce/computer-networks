import socket
import pickle


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

data = client_socket.recv(1024)
array = pickle.loads(data)

sorted_array = bubble_sort(array)

data = pickle.dumps(sorted_array)
client_socket.send(pickle.dumps("bubble"))
client_socket.send(data)

client_socket.close()
