import socket
from ftplib import FTP
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def handle_client_connection(client_socket):
    with open('received_file_socket.txt', 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
    client_socket.close()


def start_ftp_server():
    ftp_server = FTPServer((IP, PORT), FTPHandler)
    ftp_server.serve_forever()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print(f'Socket server listening on port {PORT}')

    start_ftp_server()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr[1]} is connected to the server!")
        handle_client_connection(client_socket)


if __name__ == '__main__':
    main()
