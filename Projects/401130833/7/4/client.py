import socket

def key_value_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12348))
    print("Connected to Key-Value Server...")
    try:
        while True:
            command = input("Enter command (SET/GET key [value]): ").strip()
            if command.lower() == 'exit':
                break
            client_socket.send(command.encode())
            response = client_socket.recv(1024).decode()
            print(f"Response: {response}")
    finally:
        client_socket.send(b"exit")
        client_socket.close()
        print("Disconnected from server.")

if __name__ == "__main__":
    key_value_client()
