import socket
import threading

SERVER_IP = '127.0.0.7'
SERVER_PORT = 8080

def stalin_sort(numbers):
    sorted_numbers = [int(num) for num in numbers.split()]
    disorder_detected = False
    sorted_list = [sorted_numbers[0]]
    removed_elements = []  
    for num in sorted_numbers[1:]:
        if num >= sorted_list[-1]:
            sorted_list.append(num)
        else:
            disorder_detected = True
            removed_elements.append(num)  
    return ' '.join(map(str, sorted_list)), disorder_detected, removed_elements

def handle_client(client_socket, client_address):
    received_numbers = []  
    try:
        while True:
            numbers = client_socket.recv(1024).decode()
            if numbers == '0':
                break
            
            received_numbers.extend(map(int, numbers.split()))  
            
            sorted_numbers_str, disorder_detected, removed_elements = stalin_sort(numbers)
            client_socket.sendall(sorted_numbers_str.encode())
            
            client_ip, client_port = client_address  
            
            for removed_element in removed_elements:
                message = f"Out-of-order element detected and removed: {removed_element} \n"
                client_socket.sendall(message.encode())
            
            if disorder_detected:
                client_socket.sendall(b"Disorder detected")
        

        print(f"Numbers received from {client_ip}:{client_port}: {received_numbers}")
    except ConnectionResetError:
        print(f"Connection with {client_address} closed.")
        client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print("Server is listening...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

server_socket.close()
