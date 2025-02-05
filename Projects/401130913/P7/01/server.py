import socket
import os

# Configuration
HOST = "0.0.0.0"
PORT = 21  # FTP typically uses 21, but this is a custom implementation
SHARED_FOLDER = "./shared_files"  # Change this to your preferred directory

def list_files():
    """Returns a list of files in the shared folder."""
    return "\n".join(os.listdir(SHARED_FOLDER)) or "No files available."

def handle_client(conn):
    """Handles client requests for file listings and downloads."""
    while True:
        request = conn.recv(1024).decode()
        if not request:
            break

        if request.lower() == "list":
            conn.send(list_files().encode())
        
        elif request.startswith("get "):
            filename = request[4:].strip()
            file_path = os.path.join(SHARED_FOLDER, filename)

            if os.path.exists(file_path):
                conn.send(b"OK")
                with open(file_path, "rb") as file:
                    conn.sendall(file.read())
            else:
                conn.send(b"File not found.")

    conn.close()

def start_server():
    """Starts the TCP file sharing server."""
    os.makedirs(SHARED_FOLDER, exist_ok=True)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"File server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Client connected: {addr}")
        handle_client(conn)

if __name__ == "__main__":
    start_server()
