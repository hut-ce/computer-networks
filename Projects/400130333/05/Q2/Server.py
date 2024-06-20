import socket
import threading

IP = '127.0.0.1'
PORT = 5050
deleted_number_lock = threading.Lock()

def stalin_sort(arr):
    i = 1
    while i < len(arr):
        if arr[i] < arr[i - 1]:
            with deleted_number_lock:
                deleted_number.append(arr[i])
            del arr[i]
        else:
            i += 1
    return arr

def handle_client(connection, address):
    print(f"Connection from {address}")
    while True:
        data = connection.recv(1024).decode('utf-8')
        if not data:
            print('Error!')
            break
        else:
            numbers = [int(x) for x in data.split(',')]
            if 0 in numbers:
                print(f"Received array from {address}: {numbers}")
                sorted_numbers = stalin_sort(numbers)
                print(f"Sorted array with Stalin Sort: {sorted_numbers}")
                with deleted_number_lock:
                    deleted_numbers = deleted_number.copy()
                connection.send(str(deleted_numbers).encode('utf-8'))
                connection.send(str(sorted_numbers).encode('utf-8'))
                with deleted_number_lock:
                    deleted_number.clear()  
            else:
                print(f"Received array from {address}: {numbers}")

    connection.close()


def start_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()
    print(f"Server is Running on IP:{ip}|PORT:{port}")

    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

        

if __name__ == "__main__":
    deleted_number = []
    start_server(IP, PORT)
