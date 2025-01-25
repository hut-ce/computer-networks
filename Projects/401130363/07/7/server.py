import socket
import ssl

def start_secure_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 12355))
    sock.listen(5)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    print("Server is ready for secure communication...")
    connection, address = context.wrap_socket(sock, server_side=True).accept()
    print(f"Connection established with {address}")

    while True:
        client_message = connection.recv(1024).decode()
        if not client_message or client_message.lower() == 'exit':
            print("Connection closed.")
            break
        print(f"Client: {client_message}")
        server_response = input("Server: ")
        connection.send(server_response.encode())

    connection.close()
    sock.close()

if __name__ == "__main__":
    start_secure_server()
