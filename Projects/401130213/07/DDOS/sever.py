import socket
import threading
import time

MAX_REQUESTS = 100
TIME_WINDOW = 10

clients = {}

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def handle_client_connection(client_socket, addr):
    global clients
    ip = addr[0]
    clients[ip] = clients.get(ip, 0) + 1

    if clients[ip] > MAX_REQUESTS:
        print(f"Blocking IP: {ip}")
        client_socket.close()
    else:
        time.sleep(TIME_WINDOW)
        clients[ip] -= 1

        client_socket.sendall(b'Connection accepted')
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print("Server is Running and is waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr[1]} is connected to the server!")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket, addr))
        client_handler.start()


if __name__ == '__main__':
    main()
