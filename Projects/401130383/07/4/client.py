import socket


def client(host='127.0.0.1', port=8020):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        while True:
            command = input('Enter command (GET, SET, DELETE): ')
            if command.upper() == 'EXIT':
                break

            client_socket.send(command.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print('Response:', response)


if __name__ == '__main__':
    client()

