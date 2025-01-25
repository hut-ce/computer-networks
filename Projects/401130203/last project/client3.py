import socket
def start_client(host="127.0.0.1", port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server... Waiting for currency updates...")

    try:
        while True:

            data = client_socket.recv(1024).decode("utf-8")
            print("Received data:", data)
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
