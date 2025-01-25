import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, port))
    server_socket.listen(5)
    print(f'Server listening on port {port}')
    while True:
        client_socket, addr = server_socket.accept()
        print(f"{client_socket} is connected to the server!")
        client_socket.close()


def main():
    ports = [8000, 8001, 8002]
    threads = []

    for port in ports:
        thread = threading.Thread(target=start_server, args=(port,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
