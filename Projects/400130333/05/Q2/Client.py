import socket

IP = '127.0.0.1'
PORT = 5050

def send_array_to_server(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print(f"Connected to server IP:{ip}|PORT:{port}")

    while True:
        numbers = input("Enter a list of numbers separated by comma (0 = end): ")
        if numbers == '0':
            client.send(numbers.encode())
        else:
            client.send(numbers.encode())
            deleted_number = client.recv(1024).decode('utf-8')
            sorted_numbers = client.recv(1024).decode('utf-8')
            print(f"Deleted Number: {deleted_number}\nSorted array received from server: {sorted_numbers}")

    client.close()

if __name__ == "__main__":
    send_array_to_server(IP, PORT)

