import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_ip = input("Enter the server IP address: ")
    client.connect((server_ip, 9999))
    
    user_input = input("Enter an array of numbers separated by spaces: ")
    client.send(user_input.encode())
    response = client.recv(4096).decode()
    print(f"Sorted results from server: {response}")

    client.close()

if __name__ == "__main__":
    main()
