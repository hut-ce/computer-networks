import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(("127.0.0.1", 45))
        print("Connected to the server.")
        while True:
            command = input("Enter or exit")
            client_socket.send(command.encode())
            if command.lower() == "exit":
                print("disconnected")
                break

            result = client_socket.recv(4096).decode()
            print(f"result:\n{result}")
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
