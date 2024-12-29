import socket
from datetime import datetime


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5053

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((HOST, PORT))
    client.listen(1)
    print("SO-3 (Bubble Sort) is listening...")
    while True:
        CONNECTION, ADDR = client.accept()
        print(f"Connected to {ADDR}")

        data = CONNECTION.recv(1024).decode()
        arr = list(map(int, data[1:-1].split(',')))
        start_time = datetime.now()
        sorted_arr = bubble_sort(arr)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        result = (" ".join(map(str, sorted_arr))) + f" | {duration:.8f} seconds"
        CONNECTION.send(result.encode())
        CONNECTION.close()
        print("SO-3 has finished execution.")


if __name__ == "__main__":
    main()
