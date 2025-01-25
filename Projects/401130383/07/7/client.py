import socket
import ssl

def secure_chat_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile='server.crt')

    secure_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    secure_socket.connect(('localhost', 12355))
    print("Secure connection established with the server.")

    while True:
        message = input("Client: ")
        secure_socket.send(message.encode())
        if message.lower() == 'exit':
            break
        response = secure_socket.recv(1024).decode()
        print(f"Server: {response}")

    secure_socket.close()

if __name__ == "__main__":
    secure_chat_client()
