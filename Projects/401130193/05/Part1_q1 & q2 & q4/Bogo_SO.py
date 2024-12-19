import socket
import random
from datetime import datetime


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def bogo_sort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5052

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((HOST, PORT))
    client.listen(1)
    print("SO-2 (Bogo Sort) is listening...")
    while True:
        CONNECTION, ADDR = client.accept()
        print(f"Connected to {ADDR}")

        data = CONNECTION.recv(1024).decode()
        arr = list(map(int, data[1:-1].split(',')))
        start_time = datetime.now()
        sorted_arr = bogo_sort(arr)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        result = (" ".join(map(str, sorted_arr))) + f" | {duration:.8f} seconds"
        CONNECTION.send(result.encode())
        CONNECTION.close()
        print("SO-2 has finished execution.")


if __name__ == "__main__":
    main()
