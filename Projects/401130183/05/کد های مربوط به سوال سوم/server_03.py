import socket
import threading

def handle_client(client_socket, address):
    print(f"Connected to: {address}")
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            array = list(map(int, data.split(',')))
            print(f"Received array from {address}: {array}")
            
            sorted_array = sorted(array)
            print(f"Sorted array for {address}: {sorted_array}")
            
            client_socket.send(','.join(map(str, sorted_array)).encode('utf-8'))
        except Exception as e:
            print(f"Error with {address}: {e}")
            break
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))
server.listen(3)  
print("Server is listening...")

while True:
    client_socket, address = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()