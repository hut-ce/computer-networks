import socket
import threading


# file data form: FILE:<file name>:<file data>
def send(client_socket: socket.socket):
    print('Enter Message (or "sendfile <path>" to send a file):')
    while True:
        try:
            user_input = input()
            client_socket.sendall(user_input.encode())
        except ConnectionRefusedError as e:
            print(f'send error: {e}')
            break                


def receive(client_socket: socket.socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print("Connection closed by server")
                break
            
            if data.startswith('you-are-dead'):
                print(data)
                break
            
            print(data.decode())

        except ConnectionResetError as e:
            print(f'receive erorr: {e}')
            break
        

def client_program():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('127.0.0.1', 8010))
        print('CONNECTED TO locallhost:8010')

        threading.Thread(target=receive, args=(client,)).start()
        send(client)


if __name__ == '__main__':
    client_program()
