import socket
import ssl

def run_tls_client():
    """Connects to a secure server using SSL/TLS."""
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.load_verify_locations(cafile='server_certificate.pem')

    secure_sock = tls_context.wrap_socket(client_sock, server_hostname='localhost')
    secure_sock.connect(('localhost', 12500))
    print("[CLIENT] Secure connection established with the server.")

    while True:
        client_message = input("[CLIENT]: ")
        secure_sock.send(client_message.encode())
        if client_message.lower() == 'exit':
            break
        server_response = secure_sock.recv(1024).decode()
        print(f"[SERVER]: {server_response}")

    secure_sock.close()

if __name__ == "__main__":
    run_tls_client()
