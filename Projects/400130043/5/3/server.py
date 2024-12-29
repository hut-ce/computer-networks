import socket
import threading

def handle_client(client_socket):
    while True:
        try:
          
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            numbers = list(map(int, data.split()))
            sorted_numbers = sorted(numbers)
            client_socket.send(' '.join(map(str, sorted_numbers)).encode())
        except Exception as e:
            print(f"Error: {e}")
            break
    
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    server.bind(('0.0.0.0', 9999))
    server.listen(3) 
       ip_address = socket.gethostbyname(socket.gethostname())
    print(f"Server is listening on {ip_address}:9999...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()