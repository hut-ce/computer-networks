import socket
import ssl

def run_tls_server():
    """Starts a secure server using SSL/TLS."""
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('localhost', 12500))
    server_sock.listen(5)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='server_certificate.pem', keyfile='private_key.pem')

    print("[SERVER] Waiting for secure client connections...")
    secure_conn, client_addr = ssl_context.wrap_socket(server_sock, server_side=True).accept()
    print(f"[SERVER] Secure connection established with {client_addr}")

    while True:
        message_from_client = secure_conn.recv(1024).decode()
        if not message_from_client or message_from_client.lower() == 'exit':
            print("[SERVER] Connection closed by the client.")
            break
        print(f"[CLIENT]: {message_from_client}")
        server_reply = input("[SERVER]: ")
        secure_conn.send(server_reply.encode())

    secure_conn.close()
    server_sock.close()

if __name__ == "__main__":
    run_tls_server()
