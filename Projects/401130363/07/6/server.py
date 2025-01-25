import socket
from collections import defaultdict
import time

REQUEST_LIMIT = 5  
BLOCK_DURATION = 10

def start_ddos_protection_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12354))
    server_socket.listen(5)
    print("Server is monitoring for potential DDoS attacks...")

    request_log = defaultdict(lambda: [0, time.time()])
    blocked_ips = {}

    while True:
        conn, addr = server_socket.accept()
        client_ip = addr[0]
        current_time = time.time()

        if client_ip in blocked_ips:
            if current_time - blocked_ips[client_ip] < BLOCK_DURATION:
                conn.send(b"Temporarily blocked due to high request volume.")
                conn.close()
                continue
            else:
                del blocked_ips[client_ip]

        if current_time - request_log[client_ip][1] > 1:
            request_log[client_ip] = [1, current_time]
        else:
            request_log[client_ip][0] += 1

        if request_log[client_ip][0] > REQUEST_LIMIT:
            print(f"Blocking {client_ip} for excessive request volume.")
            blocked_ips[client_ip] = current_time
            conn.send(b"Blocked due to excessive requests.")
            conn.close()
            continue

        conn.send(b"Request received successfully.")
        conn.close()

if __name__ == "__main__":
    start_ddos_protection_server()
