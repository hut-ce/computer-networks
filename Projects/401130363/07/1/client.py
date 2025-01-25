import socket
import threading
import os
import base64

def transmit_data(client_socket: socket.socket):
    print('Enter message or "sendfile <path>" to transmit a file:')
    while True:
        try:
            user_input = input()
            if user_input.startswith('sendfile'):
                path = user_input.split()[1]
                file_name = path.split('/')[-1]
                if os.path.exists(path):
                    with open(path, 'rb') as file:
                        file_content = file.read()
                    client_socket.sendall(b'FILE:' + file_name.encode() + b':' + base64.b64encode(file_content))
                else:
                    print('File not found!')
            else:
                client_socket.sendall(user_input.encode())
        except ConnectionRefusedError as e:
            print(f'Transmission error: {e}')
            break

def receive_data(client_socket: socket.socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                print("Server closed the connection")
                break
            
            if data.decode().startswith('FILE:'):
                file_name = data.decode().split(':')[1]
                with open(file_name, 'wb') as file:
                    file.write(base64.b64decode(data[5+len(file_name):]))
                    print(f'File {file_name} received successfully')
            else:
                print(data.decode())
        except ConnectionResetError as e:
            print(f'Reception error: {e}')
            break

def client_application():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 2000))
        print('Connected to localhost:2000')

        threading.Thread(target=receive_data, args=(client_socket,)).start()
        transmit_data(client_socket)

if __name__ == '__main__':
    client_application()
