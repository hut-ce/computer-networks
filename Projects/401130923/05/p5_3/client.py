import socket

HOST = '127.0.0.1'
PORT = 12345

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    numbers = input("Enter an array of numbers (space-separated): ")
    client.send(numbers.encode())
    sorted_numbers = client.recv(1024).decode()
    print(sorted_numbers)
    client.close()

if __name__ == "__main__":
    main()
