import socket

def client_application():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the server
            client_socket.connect(('127.0.0.1', 8010))
            print("Connected to server at 127.0.0.1:8010")

            # Send request for cryptocurrency prices
            client_socket.sendall('prices'.encode())

            # Receive and display server response
            response = client_socket.recv(2048).decode()
            print("Server response:")
            print(response)

    except ConnectionRefusedError:
        print("Error: Unable to connect to the server. Please check if the server is running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    client_application()
