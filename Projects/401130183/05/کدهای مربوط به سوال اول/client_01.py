import socket
import random

def stalin_sort(arr):
    result = [arr[0]]
    for num in arr[1:]:
        if num >= result[-1]:
            result.append(num)
    return result

def bogo_sort(arr):
    def is_sorted(lst):
        return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

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

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    is_first_client = input("Are you the first client? (yes/no): ").strip().lower()
    if is_first_client == 'yes':
        array = input("Enter an array of numbers separated by commas: ")
        client_socket.send(array.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
    else:
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {response}")
        if "Algorithm" in response:
            array_str, algorithm = response.split(";")
            array = list(map(int, array_str.split(":")[1].strip()[1:-1].split(',')))
            algorithm = algorithm.split(":")[1].strip()

            if algorithm == "Stalin Sort":
                sorted_array = stalin_sort(array)
            elif algorithm == "Bogo Sort":
                sorted_array = bogo_sort(array)
            elif algorithm == "Bubble Sort":
                sorted_array = bubble_sort(array)
            else:
                sorted_array = array

            print(f"Sorted Array using {algorithm}: {sorted_array}")
    
    client_socket.close()

if __name__ == "__main__":
    client_program()

