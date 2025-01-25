import socket
import threading
def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen(1)
    print(f"Server is running on port {port}")
    while True:
        client_socket, addr = server.accept()
        print(f"Connection received on port {port} from {addr}")
        client_socket.send(f"Port {port} is open.".encode('utf-8'))
        client_socket.close()

open_ports = [5000, 5001, 5002, 5003]

for port in open_ports:
    threading.Thread(target=start_server, args=(port,)).start()
