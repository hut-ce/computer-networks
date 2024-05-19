import socket

ip = '127.0.0.10'
port = 5050

def send_numbers(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print(f"Connected to Server: ({ip}/{port})")

    while True:
        numbers = input("Enter numbers (Separated with comma and Enter 0 for End): ")
        if numbers == '0':
            client.send(numbers.encode('utf-8'))
        else:
            client.send(numbers.encode())
            deleted_numbers = client.recv(1024).decode('utf-8')
            sorted_numbers = client.recv(1024).decode('utf-8')
            print(f"Deleted Numbers: {deleted_numbers}\nSorted Array: {sorted_numbers}")

    client.close()

if __name__ == "__main__":
    send_numbers(ip, port)

