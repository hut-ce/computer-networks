import socket
import threading
import random

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP, PORT))


def stalin_sort(array):
    if not array:
        return []
    sorted_list = [array[0]]
    for i in range(1, len(array)):
        if array[i] >= sorted_list[-1]:
            sorted_list.append(array[i])
        return sorted_list


def is_sorted(arr):
    """Helper function to check if the list is sorted."""
    return all(arr[i] <= arr[i+1] for i in range(len(arr) - 1))


def bogosort(arr):
    """Shuffles the array until it is sorted."""
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr


def bubble_sort(arr):
    n = len(arr)

    for i in range(n):

        for j in range(0, n-i-1):

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def receive_message(client):
    while True:
        try:
            command, sorting_index_str = (client.recv(1024).decode()).split(" ")
            if command == "answer":
                sorting_index = int(sorting_index_str)
                if not sorting_index:
                    break
                message = client.recv(1024).decode()
                if not message:
                    break
                if sorting_index == 1:
                    sorted_array = stalin_sort(message.split(","))
                elif sorting_index == 2:
                    sorted_array = bogosort(message.split(","))
                elif sorting_index == 3:
                    sorted_array = bubble_sort(message.split(","))
                else:
                    raise Exception("no sorting algorithm that match the index given is available!")

                message_to_send = ",".join(map(str, sorted_array))
                client.send("answer".encode('utf-8'))
                client.send(f"{message_to_send}".encode('utf-8'))
            elif command == "confirmation":
                message = client.recv(1024).decode()
                if not message:
                    break
                print(message)

        except ConnectionResetError:
            print("Connection with the server is lost!")
            break
        except ConnectionAbortedError:
            break


thread = threading.Thread(target=receive_message, args=(client,))
thread.start()

try:
    while True:
        message = input("Please enter your array: \n")
        client.send("sort".encode('utf-8'))
        client.send(f"{message}".encode('utf-8'))
except KeyboardInterrupt:
    print("Connection is closing...")
    client.close()

