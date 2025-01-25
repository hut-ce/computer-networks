import socket

def remote_command_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12346))
    print("Connected to Command Execution Server...")
    while True:
        command = input("Enter command to execute: ").strip()
        if command.lower() == 'exit':
            client_socket.send(b'exit')
            break
        client_socket.send(command.encode())
        result = client_socket.recv(4096).decode()
        print(f"Command Output:\n{result}")
    client_socket.close()

if __name__ == "__main__":
    remote_command_client()
