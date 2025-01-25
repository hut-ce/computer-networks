import socket


IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print(data)

    client_socket.close()


if __name__ == '__main__':
    main()
