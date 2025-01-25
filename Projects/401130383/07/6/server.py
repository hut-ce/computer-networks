import socket
from collections import defaultdict
import time

THRESHOLD = 5  
BLOCK_TIME = 10

def ddos_detection_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12354))
    server_socket.listen(5)
    print("DDOS Detection Server is listening...")

    request_counts = defaultdict(lambda: [0, time.time()])
    blocked_clients = {}

    while True:
        conn, addr = server_socket.accept()
        client_ip = addr[0]
        current_time = time.time()

        if client_ip in blocked_clients:
            if current_time - blocked_clients[client_ip] < BLOCK_TIME:
                conn.send(b"You are temporarily blocked due to excessive requests.")
                conn.close()
                continue
            else:
                del blocked_clients[client_ip]

        if current_time - request_counts[client_ip][1] > 1:
            request_counts[client_ip] = [1, current_time]
        else:
            request_counts[client_ip][0] += 1

        if request_counts[client_ip][0] > THRESHOLD:
            print(f"Blocking {client_ip} due to excessive requests.")
            blocked_clients[client_ip] = current_time
            conn.send(b"You have been blocked due to excessive requests.")
            conn.close()
            continue

        conn.send(b"Request received.")
        conn.close()

if __name__ == "__main__":
    ddos_detection_server()
