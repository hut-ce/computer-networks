import socket
import time
from collections import defaultdict

MAX_REQUESTS = 5  # حداکثر تعداد درخواست‌ها در هر ثانیه
BLOCK_TIME = 10   # مدت زمان بلاک شدن (ثانیه)

def ddos_protection_server():
    """Starts a server to monitor and prevent DDoS attacks."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('localhost', 12400))
        server.listen(5)
        print("[SERVER] Monitoring started for DDoS attacks...")

        request_tracker = defaultdict(lambda: [0, time.time()])
        blocked_ips = {}

        while True:
            client_conn, client_addr = server.accept()
            client_ip = client_addr[0]
            current_time = time.time()

            # Handle blocked IPs
            if client_ip in blocked_ips:
                if current_time - blocked_ips[client_ip] < BLOCK_TIME:
                    client_conn.send(b"[ERROR] You are temporarily blocked.")
                    client_conn.close()
                    continue
                else:
                    del blocked_ips[client_ip]

            # Update request tracker
            if current_time - request_tracker[client_ip][1] > 1:
                request_tracker[client_ip] = [1, current_time]
            else:
                request_tracker[client_ip][0] += 1

            # Check for excessive requests
            if request_tracker[client_ip][0] > MAX_REQUESTS:
                print(f"[WARNING] Blocking {client_ip} due to excessive requests.")
                blocked_ips[client_ip] = current_time
                client_conn.send(b"[ERROR] Too many requests. You are now blocked.")
                client_conn.close()
                continue

            # Process valid request
            client_conn.send(b"[SUCCESS] Request processed.")
            client_conn.close()

if __name__ == "__main__":
    ddos_protection_server()
