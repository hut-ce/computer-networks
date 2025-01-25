import os
import socket

def list_files(conn):
    files = ";".join(os.listdir("."))
    conn.send(files.encode())

def upload_file(conn, filename):
    with open(filename, "wb") as f:
        while True:
            data = conn.recv(1024)
            if data == b"EOF":
                break
            f.write(data)
    conn.send(f"{filename} uploaded successfully.".encode())

def download_file(conn, filename):
    try:
        with open(filename, "rb") as f:
            while chunk := f.read(1024):
                conn.send(chunk)
        conn.send(b"EOF")
    except FileNotFoundError:
        conn.send(f"Error: {filename} not found.".encode())

def handle_client(conn):
    while True:
        command = conn.recv(1024).decode()
        if not command or command.lower() == 'exit':
            print("Closing connection...")
            break
        if command.startswith("LIST"):
            list_files(conn)
        elif command.startswith("UPLOAD"):
            _, filename = command.split(" ", 1)
            upload_file(conn, filename)
        elif command.startswith("DOWNLOAD"):
            _, filename = command.split(" ", 1)
            download_file(conn, filename)
        else:
            conn.send(b"Invalid command.")

def ftp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("FTP Server is listening...")
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")
    handle_client(conn)
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    ftp_server()
