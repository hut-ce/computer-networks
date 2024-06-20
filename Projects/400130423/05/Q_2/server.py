import socket
import threading

clients = {}  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.5'
port = 5050
server_socket.bind((host, port))
server_socket.listen()
print('server is running...')

def stalin_sort(arr, client):
    n = len(arr)
    i = 0
    while i < n - 1:
        if arr[i] > arr[i + 1]:
            removed_number = arr[i]
            del arr[i]
            n -= 1
            if i > 0:
                i -= 1
            client.send(f"number {removed_number} removed\n".encode())  
        else:
            i += 1
    return arr

def handle_client(client, addr):
    print(f'{addr} is connected to the server...')
    
    clients[addr] = client
    
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        numbers = [int(x) for x in data.split(',')]
        hostname = addr[0]
    
        if 0 in numbers:
            client.send(hostname.encode())
        client.send(hostname.encode())

        sorted_numbers = stalin_sort(numbers, client)
        client.send(','.join(map(str, sorted_numbers)).encode())
    client.close()

    del clients[addr]

while True:
    client, addr = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client, addr))
    client_handler.start()
