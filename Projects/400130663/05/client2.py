import socket

SERVER_IP = '127.0.0.7'
SERVER_PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

try:
    while True:
        numbers = input("Enter a list of numbers (separated by spaces), 0 to exit: ")
        client_socket.sendall(numbers.encode())

        if numbers == '0':
            
            break

        sorted_numbers_str = client_socket.recv(1024).decode()
        print("Sorted array:", sorted_numbers_str)
        

        disorder_message = client_socket.recv(1024).decode()
        if disorder_message:
            print(disorder_message)

except KeyboardInterrupt:
    print("\nExiting...")

client_socket.close()
