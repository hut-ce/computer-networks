import socket
import threading

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Server started on port {port}")
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        client_socket.close()

if __name__ == "__main__":
    ports = [8000, 8001, 8002]
    for port in ports:
        threading.Thread(target=start_server, args=(port,)).start()
