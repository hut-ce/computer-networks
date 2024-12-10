import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostbyname()
    IP =(socket.gethostbyname(hostname),9999)

    client.connect(IP)
    user_input = input("Enter an array of numbers separated by spaces: ")
    client.send(user_input.encode())

    response = client.recv(4096).decode()
    print(f"Sorted results from server: {IP}")

    client.close()

if __name__ == "__main__":
    main()
