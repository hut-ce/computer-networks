import socket
import random

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
#کدهایی که در صورت سواال داده شده
def is_sorted(arr):
    """Helper function to check if the list is sorted."""
    return all(arr[i] <= arr[i+1] for i in range(len(arr) - 1))
def bogosort(arr):
    """Shuffles the array until it is sorted."""
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def stalin_sort(arr):
    if not arr:
        return []
    sorted_list = [arr[0]]
    for i in range(1, len(arr)):
        if arr[i] >= sorted_list[-1]:
            sorted_list.append(arr[i])
    return sorted_list

def client_sender_program():
    host = socket.gethostbyname(socket.gethostname)
    port = 5050
    client_socket = socket.socket()
    client_socket.connect((host, port))
    array = list(map(int, input("Enter the array (space-separated): ").split()))
    array_data = ','.join(map(str, array))
    client_socket.send(array_data.encode())
    sorted_arrays_data = client_socket.recv(1024).decode()
    print(f"Sorted arrays received from server: {sorted_arrays_data}")
    client_socket.close()

def so_program(algorithm):
    host = socket.gethostbyname(socket.gethostname)
    port = 5050

    client_socket = socket.socket()
    client_socket.connect((host, port))

    array_data = client_socket.recv(1024).decode()
    array = list(map(int, array_data.split(',')))
    print(f"SO received array: {array}")
    if algorithm == "bubble":
        sorted_array = bubble_sort(array)
    elif algorithm == "stalin":
        sorted_array = stalin_sort(array)
    elif algorithm == "bogo":
        sorted_array = bogosort(array)
    else:
        sorted_array = array


    sorted_data = ','.join(map(str, sorted_array))
    client_socket.send(sorted_data.encode())
    client_socket.close()
if __name__ == "__main__":
    role = input("Enter 'c' for client or 'so' for sorting client: ").strip().lower()
    if role == 'c':
        client_sender_program()
    elif role == 'so':
        so_program()
    else:
        print("invaid!")
