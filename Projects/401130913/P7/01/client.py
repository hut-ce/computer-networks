import socket

# Server configuration
SERVER_HOST = "127.0.0.1"  # Change to actual server IP if needed
SERVER_PORT = 21

def list_files(client):
    """Requests and prints the list of available files."""
    client.send("list".encode())
    file_list = client.recv(4096).decode()
    print("Available files:\n" + file_list)

def download_file(client, filename):
    """Requests a file from the server and saves it locally."""
    client.send(f"get {filename}".encode())
    
    response = client.recv(1024)
    if response == b"OK":
        with open(filename, "wb") as file:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                file.write(data)
        print(f"File '{filename}' downloaded successfully.")
    else:
        print("File not found on server.")

def main():
    """Handles user input for interacting with the server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    while True:
        command = input("Enter command (list, get <filename>, exit): ").strip().lower()
        if command == "exit":
            break
        elif command == "list":
            list_files(client)
        elif command.startswith("get "):
            filename = command[4:].strip()
            if filename:
                download_file(client, filename)
            else:
                print("Please provide a filename.")
        else:
            print("Invalid command.")

    client.close()

if __name__ == "__main__":
    main()
