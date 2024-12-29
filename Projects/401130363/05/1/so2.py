import socket
import pickle
import random


def bogo_sort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

data = client_socket.recv(1024)
array = pickle.loads(data)

sorted_array = bogo_sort(array)

data = pickle.dumps(sorted_array)
client_socket.send(pickle.dumps("bogo"))
client_socket.send(data)

client_socket.close()
