import socket
import ssl

def secure_chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12355))
    server_socket.listen(5)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    print("Secure Chat Server is listening...")
    conn, addr = context.wrap_socket(server_socket, server_side=True).accept()
    print(f"Secure connection established with {addr}")

    while True:
        message = conn.recv(1024).decode()
        if not message or message.lower() == 'exit':
            print("Client disconnected.")
            break
        print(f"Client: {message}")
        response = input("Server: ")
        conn.send(response.encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    secure_chat_server()
