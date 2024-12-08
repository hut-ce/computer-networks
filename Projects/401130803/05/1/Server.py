import socket
import threading
import random

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def bogo_sort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def stalin_sort(arr):
    result = [arr[0]]
    for num in arr[1:]:
        if num >= result[-1]:
            result.append(num)
    return result

def handle_client(connection, addr):
    print(f"Connected to {addr}")
    while True:
        arrNumber = connection.recv(1024).decode('utf-8')
        if not arrNumber:
            print(f"Connection with {addr} is closed")
            break
        print(f"{arrNumber} received from {addr}")
        arr = eval(arrNumber)
        sorted_arr = bubble_sort(arr)  # You can change the sorting algorithm here
        connection.send(str(sorted_arr).encode('utf-8'))
    connection.close()

def main():
    IP = socket.gethostbyname(socket.gethostname())
    Port = 5050
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, Port))
    server.listen(5)
    print("SERVER is running")

    while True:
        connection, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, addr))
        thread.start()

if __name__ == "__main__":
    main()
