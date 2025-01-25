import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    while True:
        domain = input("Enter domain name to resolve (or 'exit' to quit): ")
        if domain.lower() == 'exit':
            break
        client_socket.sendall(domain.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"IP Address for '{domain}' you entered is: {response}")

    client_socket.close()


if __name__ == '__main__':
    main()
