import socket
import ssl

def start_secure_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 10000))
    server.listen(5)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    print("Secure Chat Server is running...")

    while True:
        conn, addr = server.accept()
        secure_conn = context.wrap_socket(conn, server_side=True)
        print(f"Secure connection from {addr}")
        secure_conn.send(b"Welcome to Secure Chat Room.")
        secure_conn.close()

if __name__ == "__main__":
    start_secure_server()
import socket
import ssl

def start_secure_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 10000))
    server.listen(5)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    print("Secure Chat Server is running...")

    while True:
        conn, addr = server.accept()
        secure_conn = context.wrap_socket(conn, server_side=True)
        print(f"Secure connection from {addr}")
        secure_conn.send(b"Welcome to Secure Chat Room.")
        secure_conn.close()

if __name__ == "__main__":
    start_secure_server()
