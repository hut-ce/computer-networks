import socket
import threading
import os
import base64

def send_to_server(socket_conn: socket.socket):
    print('Type a message or use "upload <file_path>" to send a file:')
    while True:
        try:
            user_input = input()
            if user_input.startswith('upload'):
                file_path = user_input.split()[1]
                file_name = os.path.basename(file_path)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    socket_conn.sendall(b'FILE:' + file_name.encode() + b':' + base64.b64encode(file_data))
                else:
                    print('Error: File does not exist.')
            else:
                socket_conn.sendall(user_input.encode())
        except ConnectionRefusedError as error:
            print(f"Error during sending: {error}")
            break

def receive_from_server(socket_conn: socket.socket):
    while True:
        try:
            server_data = socket_conn.recv(4096)
            if not server_data:
                print("Connection to the server was closed.")
                break

            if server_data.decode().startswith('FILE:'):
                file_info = server_data.decode().split(':', 2)
                file_name = file_info[1]
                file_content = base64.b64decode(file_info[2])
                with open(file_name, 'wb') as output_file:
                    output_file.write(file_content)
                print(f"File {file_name} downloaded successfully.")
            else:
                print(server_data.decode())
        except ConnectionResetError as error:
            print(f"Error during receiving: {error}")
            break

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_conn:
        client_conn.connect(('127.0.0.1', 2000))
        print("Connected to the server at 127.0.0.1:2000")

        threading.Thread(target=receive_from_server, args=(client_conn,)).start()
        send_to_server(client_conn)

if __name__ == '__main__':
    run_client()
