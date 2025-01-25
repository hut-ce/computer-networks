import socket


def client_program():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            # Connecting to the server.
            client.connect(('127.0.0.1', 8010))
            print('Connected to Server: locahost:8010')

            # Sending message.
            client.send('rates'.encode())

            # Receiving responce.
            try:
                print(client.recv(1024).decode())
            except ConnectionResetError as e:
                print(f'Error receiving data: {e}')

        print('Closed connection!')
    except ConnectionResetError as e:
        print(f'Error Client disconnected: {e}')


if __name__ == '__main__':
    client_program()
