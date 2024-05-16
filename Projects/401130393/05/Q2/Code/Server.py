import socket
import threading

ip = '127.0.0.5'
port = 5050 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()

print("Server is Running and waiting for connections...")

def sort(data):
    numbers = [int(x) for x in data.split(',')]
    sorted_numbers = sorted(numbers)
    return sorted_numbers

def handle_client(connection):
    name = connection.recv(1024).decode('utf-8')
    
    while True:
        try:
            numbers = connection.recv(1024).decode('utf-8')
            if not numbers:
                break
            print(f"Received data from {name}: {numbers}")
            
            sorted_numbers = sort(numbers)
            print(f"Sorted numbers: {sorted_numbers}")
            connection.send(str(sorted_numbers).encode('utf-8'))
            
            
        except ConnectionResetError:
            print(f"Connection with {name} is closed.")
            break 
        
    connection.close()
    print(f"{name} has left!")

try:
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection,))
        thread.start()
        
except KeyboardInterrupt:
    print("Server is shutting down...")
    server.close()

