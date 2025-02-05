import socket

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))

    while True:
        command = input("Enter command (or 'exit' to quit): ")
        client.send(command.encode())
        if command.lower() == "exit":
            break
        response = client.recv(4096).decode()
        print("Output:")
        print(response)

    client.close()

if __name__ == "__main__":
    connect_to_server()
