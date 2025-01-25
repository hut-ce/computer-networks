import socket
import threading
import time
limit = 50  
window = 10 
request_counts = {}
block_list = set()
    
def handle_client(client_socket, client_address):
    global request_counts, block_list

    
    if client_address[0] in block_list:
        client_socket.send("You are blocked.".encode('utf-8'))
        client_socket.close()
        return

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Request from {client_address[0]}: {data}")
            if client_address[0] not in request_counts:
                request_counts[client_address[0]] = []
            current_time = time.time()
            request_counts[client_address[0]].append(current_time)
            request_counts[client_address[0]] = [
                timestamp for timestamp in request_counts[client_address[0]] 
                if current_time - timestamp <= window]
            if len(request_counts[client_address[0]]) > limit:
                print(f"blocking {client_address[0]} because of too many requests.")
                block_list.add(client_address[0])
                client_socket.send("You are blocked because of ddos.".encode('utf-8'))
                client_socket.close()
                break
            client_socket.send("Request received".encode('utf-8'))
        
        except Exception as error:
            print(f"The Error {error} with client {client_address}")
            break
    client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 100))
    server.listen(5)
    print("Server is Listening on 127.0.0.1:100")

    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
