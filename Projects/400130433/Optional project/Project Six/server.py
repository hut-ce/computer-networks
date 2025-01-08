import socket
import threading
import time


request_counts = {}
block_list = set()
REQUEST_LIMIT = 10  
TIME_WINDOW = 5     


def handle_client(client_socket, client_address):
    global request_counts, block_list

    
    if client_address[0] in block_list:
        client_socket.send("You are blocked.".encode())
        client_socket.close()
        return

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            print(f"Request from {client_address[0]}: {data}")
            
            
            if client_address[0] not in request_counts:
                request_counts[client_address[0]] = []
            
            
            current_time = time.time()
            request_counts[client_address[0]].append(current_time)
            
            
            request_counts[client_address[0]] = [
                timestamp for timestamp in request_counts[client_address[0]] 
                if current_time - timestamp <= TIME_WINDOW
            ]
            
            
            if len(request_counts[client_address[0]]) > REQUEST_LIMIT:
                print(f"Blocking {client_address[0]} due to too many requests.")
                block_list.add(client_address[0])
                client_socket.send("You are blocked due to DDoS behavior.".encode())
                client_socket.close()
                break
            
            
            client_socket.send("Request received".encode())
        
        except Exception as e:
            print(f"Error with client {client_address}: {e}")
            break

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("Server is running on port 8080...")

    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
