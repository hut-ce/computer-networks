import socket

ip = '127.0.0.5'  # Server IP address
PORT = 5050
flag = True
numbers = []

while flag:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, PORT))
        print("Connected to server")

        while True:
            number = input("Enter an num(int) :  (0 to send numbers): ")
            if number == '0':
                client.sendall(' '.join(map(str, numbers)).encode())
                print("Sent array to server:", numbers)
                removed_elements = client.recv(1024).decode().split()
                print("---removed number ---:")
                for removed_element in removed_elements:
                    print("Removed number:", removed_element)
                sorted_array = client.recv(1024).decode().split()
                sorted_array = list(map(int, sorted_array))  # Convert strings to integers
                print("sorted array:", sorted_array)
                break

            numbers.append(int(number))
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client.close()
