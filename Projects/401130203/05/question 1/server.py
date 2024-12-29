import socket
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
def server_program():
    host = socket.gethostbyname(socket.gethostname)
    port = 5050
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(4)  # مطمین نیستم شاید 3 باید باشه توی پرانتز
    print("Server is waiting for connections...")
    clients = []
    while len(clients) < 4:
        connection, addr = server_socket.accept()
        print(f"Connection from: {addr}")
        clients.append(connection)
    print("All conected.")
    client_sender = clients[0]
    array_data = client_sender.recv(1024).decode()
    array = list(map(int, array_data.split(',')))
    print(f"Received array from client: {array}")
    for so_client in clients[1:]:
        so_client.send(array_data.encode())
    sorted_arrays = []
    for so_client in clients[1:]:
        sorted_data = so_client.recv(1024).decode()
        sorted_array = list(map(int, sorted_data.split(',')))
        sorted_arrays.append(sorted_array)
        print(f"Received sorted array: {sorted_array}")

    client_sender.send(str(sorted_arrays).encode())
    print("Sorted arrays sent to the client.")

    for connection in clients:
        connection.close()
if __name__ == "__main__":
    server_program()



