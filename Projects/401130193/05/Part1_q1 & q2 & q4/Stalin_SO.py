import socket
import datetime


def stalin_sort(arr):
    start_time = datetime.datetime.now()
    if not arr:
        return []

    result = [arr[0]]
    for num in arr[1:]:
        if num >= result[-1]:
            result.append(num)
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    return result, duration


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5051

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((HOST, PORT))
    client.listen(1)
    print("SO-1 (Stalin Sort) is listening...")

    while True:
        CONNECTION, ADDR = client.accept()
        print(f"Connected to {ADDR}")

        data = CONNECTION.recv(1024).decode()
        arr = list(map(int, data[1: -1].split(',')))
        sorted_arr, time = stalin_sort(arr)
        result = (" ".join(map(str, sorted_arr))) + f" | {time:.10f} seconds"
        CONNECTION.send(result.encode())
        CONNECTION.close()
        print("SO-1 has finished execution.")


if __name__ == "__main__":
    main()
