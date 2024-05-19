import socket
import threading

ip = '127.0.0.10'
port = 5050
deleted_numbers_lock = threading.Lock()

def stalin_sort(arr):
    index = 1
    while index < len(arr):
        if arr[index] < arr[index - 1]:
            with deleted_numbers_lock:
                deleted_number.append(arr[index])
            del arr[index]
        else:
            index += 1
    return arr

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    while True:
        number = conn.recv(1024).decode('utf-8')
        if not number:
            print("Oops! Failed.")
            break
        else:
            numbers = [int(x) for x in number.split(',')]
            if 0 in numbers:
                print(f"Received array from {addr}: {numbers}")
                sorted_numbers = stalin_sort(numbers)
                print(f"Sorted with Stalin-Sort: {sorted_numbers}")
                with deleted_numbers_lock:
                    deleted_numbers = deleted_number.copy()
                conn.send(str(deleted_numbers).encode('utf-8'))
                conn.send(str(sorted_numbers).encode('utf-8'))
                with deleted_numbers_lock:
                    deleted_number.clear()  
            else:
                print(f"Received array from {addr}: {numbers}")

    conn.close()


def start_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()
    print(f"Server Running: ({ip}/{port})")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        

if __name__ == "__main__":
    deleted_number = []
    start_server(ip, port)
