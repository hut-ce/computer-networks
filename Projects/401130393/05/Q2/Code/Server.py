import socket
import threading

ip = '127.0.0.5'
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()

print("Server is Running and waiting for connections...")

def stalin_sort(arr, connection):
    sorted_arr = [arr[0]]
    for item in arr[1:]:
        if item >= sorted_arr[-1]:
            sorted_arr.append(item)
        else:
            connection.send(f"'{item}' has been removed from the list!\n".encode('utf-8'))
    return sorted_arr
            
        

def handle_client(connection):
    name = connection.recv(1024).decode('utf-8')
    while True:
        try:
            numbers = connection.recv(1024).decode('utf-8').split(sep= ", ")
            if not numbers:
                break
            print(f"Received data from {name}: {numbers}")
            
            sorted_numbers = stalin_sort(numbers, connection)
            
            message = f"Sorted numbers: {sorted_numbers}\n"
            print(message)
            connection.send(message.encode('utf-8'))
            
            
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
