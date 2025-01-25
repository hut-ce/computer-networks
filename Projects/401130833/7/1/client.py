import socket

def list_files(client_socket):
    client_socket.send(b"LIST")
    response = client_socket.recv(1024).decode()
    print(f"Files: {response}")

def upload_file(client_socket, filename):
    client_socket.send(f"UPLOAD {filename}".encode())
    try:
        with open(filename, "rb") as f:
            while chunk := f.read(1024):
                client_socket.send(chunk)
        client_socket.send(b"EOF")
        response = client_socket.recv(1024).decode()
        print(response)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")

def download_file(client_socket, filename):
    client_socket.send(f"DOWNLOAD {filename}".encode())
    with open(f"downloaded_{filename}", "wb") as f:
        while True:
            data = client_socket.recv(1024)
            if data == b"EOF":
                break
            f.write(data)
    print(f"{filename} downloaded successfully.")

def ftp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to FTP server...")
    while True:
        command = input("FTP Client: ").strip()
        if command.lower() == 'exit':
            client_socket.send(b"exit")
            break
        elif command.startswith("LIST"):
            list_files(client_socket)
        elif command.startswith("UPLOAD"):
            _, filename = command.split(" ", 1)
            upload_file(client_socket, filename)
        elif command.startswith("DOWNLOAD"):
            _, filename = command.split(" ", 1)
            download_file(client_socket, filename)
        else:
            print("Invalid command.")
    client_socket.close()

if __name__ == "__main__":
    ftp_client()
