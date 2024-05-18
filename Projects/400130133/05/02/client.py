import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.5'
port = 5050
client_socket.connect((host, port))

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if message:
            print(message)

def main():
    message_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    message_thread.start()
    while True:
        numbers = input("enter your numbers:\n")
        if numbers == 0:
            break
        client_socket.send(numbers.encode())
        sorted_numbers = client_socket.recv(4096).decode()
        print(sorted_numbers)

if __name__ == "__main__":
    main()
