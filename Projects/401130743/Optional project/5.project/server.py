import socket
import threading


def handle_port(port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    
    while True:

        client_socket, addr = server_socket.accept()
        print(f"Connection received on port {port} from {addr}")
        client_socket.send(f"Connected to port {port}".encode())
        client_socket.close()


def start_server():

    print("Server started.")
    ports_listen = [8080, 9090, 10000]  
    threads = []
    
    for port in ports_listen:
        thread = threading.Thread(target=handle_port, args=(port,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_server()
