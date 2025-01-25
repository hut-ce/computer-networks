import socket
import threading


# file data form: FILE:<file name>:<file data>
def send_to_server(client_socket: socket.socket):
    print('Enter Message (or "sendfile <path>" to send a file):')
    while True:
        try:
            user_input = input()
            client_socket.sendall(user_input.encode())
        except ConnectionRefusedError as err:
            print(f'send error: {err}')
            break


def receive(client_socket: socket.socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print("Connection closed...!")
                break

            if data.startswith('you-are-dead'):
                print(data)
                break

            print(data.decode())

        except ConnectionResetError as err:
            print(f'receive error: {err}')
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(('localhost', 55555))

    threading.Thread(target=receive, args=(client,)).start()
    send_to_server(client)
