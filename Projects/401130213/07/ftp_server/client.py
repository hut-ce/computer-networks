import socket
from ftplib import FTP

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def send_file_via_socket(file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.sendall(data)
    client_socket.close()


def send_file_via_ftp(file_path, username, password):
    ftp = FTP(IP)
    ftp.login(user=username, passwd=password)

    with open(file_path, 'rb') as file:
        ftp.storbinary('STOR ' + file_path, file)
    ftp.quit()


def main():
    file_path = 'file_to_send.txt'
    user_name = input("Please enter your username: ")
    password = input("Please enter your password: ")

    send_file_via_socket(file_path)

    send_file_via_ftp(file_path, user_name, password)


if __name__ == '__main__':
    main()
