import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print(f"Sorted array from server: {message}")
        except (ConnectionResetError, ConnectionAbortedError):
            print("Connection with the server was lost.")
            break


def start_client():
    threading.Thread(target=receive_messages, daemon=True).start()
    try:
        while True:
            message = input("Enter an array (comma-separated integers): ")
            client.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Closing connection...")
        client.close()


if __name__ == "__main__":
    start_client()
