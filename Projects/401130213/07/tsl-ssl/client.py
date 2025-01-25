import socket
import ssl

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def main():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('server.crt')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_client_socket = context.wrap_socket(client_socket, server_hostname=IP)

    secure_client_socket.connect((IP, PORT))

    while True:
        message = input("Enter message to send: ")
        if message.lower() in ['exit', 'quit']:
            break
        secure_client_socket.sendall(message.encode('utf-8'))
        response = secure_client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    secure_client_socket.close()


if __name__ == '__main__':
    main()
