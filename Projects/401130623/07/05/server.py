import socket
import threading

def handle_port(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection received on port {port} from {addr}")
        client_socket.send(f"Connected to port {port}".encode())
        client_socket.close()

def start():
    print("Server is started.")
    threads = []
    listen = [1, 200, 500]  
    
    for port in listen:
        thread = threading.Thread(target=handle_port, args=(port,)).append(thread).start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start()
