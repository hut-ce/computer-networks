import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(1)

    print("Server is listening...")

    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    data = client_socket.recv(1024).decode()
    numbers = [int(num) for num in data.split(",")]

    # Sort the numbers using the Stalin sort algorithm
    sorted_numbers = stalin_sort(numbers)

    # Print the sorted numbers and send them back to the client
    print(f"Sorted numbers: {sorted_numbers}")
    client_socket.send(str(sorted_numbers).encode())

    client_socket.close()
    server_socket.close()

def stalin_sort(arr):
    result = []
    max_seen = float("-inf")

    for num in arr:
        if num >= max_seen:
            result.append(num)
            max_seen = num

    return result

if __name__ == "__main__":
    main()
