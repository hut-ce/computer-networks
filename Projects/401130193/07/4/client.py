import socket


def start_client(host='127.0.0.1', port=5000):
    """Connect to the server and interact via commands."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            while True:
                command = input('Enter command (GET <key>, SET <key> <value>, REMOVE <key>, EXIT): ').strip()
                if command.upper() == 'EXIT':
                    print("Closing connection...")
                    break

                client_socket.sendall(command.encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                print('Server Response:', response)

        except ConnectionRefusedError:
            print("Error: Unable to connect to the server. Please check if the server is running.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")


if __name__ == '__main__':
    start_client()
