import socket
import threading

array_from_client = None
connected_clients = []
sorting_algorithms = ["Stalin Sort", "Bogo Sort", "Bubble Sort"]

def handle_client(client_socket, client_address, client_id):
    global array_from_client
    connected_clients.append(client_socket)
    print(f"Client connected: {client_address}")

    if array_from_client is None:
        data = client_socket.recv(1024).decode('utf-8')
        array_from_client = list(map(int, data.split(',')))
        print(f"Received array from client {client_address}: {array_from_client}")
        client_socket.send("Array received successfully!".encode('utf-8'))
    else:
        if client_id - 1 < len(sorting_algorithms):
            algorithm = sorting_algorithms[client_id - 1]
            message = f"Array: {array_from_client}; Algorithm: {algorithm}"
            client_socket.send(message.encode('utf-8'))
        else:
            client_socket.send("No sorting task assigned.".encode('utf-8'))
    
    client_socket.close()

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)
    print("Server is listening on port 5555...")

    client_id = 0
    while True:
        client_socket, client_address = server_socket.accept()
        client_id += 1
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_id))
        client_thread.start()

if __name__ == "__main__":
    server_program()
