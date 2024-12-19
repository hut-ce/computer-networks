import socket
import pickle


def stalin_sort(arr):
    sorted_arr = []
    for num in arr:
        if not sorted_arr or num >= sorted_arr[-1]:
            sorted_arr.append(num)
    return sorted_arr


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

data = client_socket.recv(1024)
array = pickle.loads(data)

sorted_array = stalin_sort(array)

data = pickle.dumps(sorted_array)
client_socket.send(pickle.dumps("stalin"))
client_socket.send(data)

client_socket.close()
