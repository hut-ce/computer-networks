import socket
import subprocess

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e)

def remote_command_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12346))
    server_socket.listen(1)
    print("Command Execution Server is listening...")
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")
    while True:
        command = conn.recv(1024).decode()
        if not command or command.lower() == 'exit':
            print("Closing connection...")
            break
        result = execute_command(command)
        conn.send(result.encode())
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    remote_command_server()
