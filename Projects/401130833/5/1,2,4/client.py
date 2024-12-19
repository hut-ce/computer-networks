import socket
import threading
import random

class SortingClient:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

    @staticmethod
    def stalin_sort(array):
        if not array:
            return []
        sorted_list = [array[0]]
        for i in range(1, len(array)):
            if array[i] >= sorted_list[-1]:
                sorted_list.append(array[i])
        return sorted_list

    @staticmethod
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    @staticmethod
    def bogosort(arr):
        while not SortingClient.is_sorted(arr):
            random.shuffle(arr)
        return arr

    @staticmethod
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def handle_server_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message.startswith("answer|"):
                    _, sorting_index, array_str = message.split("|")
                    sorting_index = int(sorting_index)
                    array = list(map(int, array_str.split(",")))
                    sorted_array = self.sort_array(sorting_index, array)
                    self.client.send(",".join(map(str, sorted_array)).encode('utf-8'))
            except (ConnectionResetError, ConnectionAbortedError):
                print("Connection lost.")
                break

    def sort_array(self, sorting_index, array):
        if sorting_index == 1:
            return self.stalin_sort(array)
        elif sorting_index == 2:
            return self.bogosort(array)
        elif sorting_index == 3:
            return self.bubble_sort(array)
        else:
            raise ValueError("Invalid sorting index.")

    def start(self):
        thread = threading.Thread(target=self.handle_server_messages)
        thread.start()
        try:
            while True:
                message = input("Enter your array (comma-separated): ")
                self.client.send(f"sort|{message}".encode('utf-8'))
        except KeyboardInterrupt:
            print("Closing connection...")
            self.client.close()

if __name__ == "__main__":
    client = SortingClient(socket.gethostbyname(socket.gethostname()), 5050)
    client.start()
