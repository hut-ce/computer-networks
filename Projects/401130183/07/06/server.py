import socket
import time

MAX_REQUESTS = 10
TIME_WINDOW = 10  
BLOCKED_IPS = set()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(5)

client_requests = {}

def cleanup():
    current_time = time.time()
    for ip in list(client_requests.keys()):
        client_requests[ip] = [t for t in client_requests[ip] if current_time - t < TIME_WINDOW]
        if not client_requests[ip]:
            del client_requests[ip]

while True:
    conn, addr = server.accept()
    ip = addr[0]
    
    cleanup()
    
    if ip in BLOCKED_IPS:
        print(f"Blocked IP {ip} tried to connect.")
        conn.close()
        continue
    
    if ip not in client_requests:
        client_requests[ip] = []
    
    client_requests[ip].append(time.time())
    
    if len(client_requests[ip]) > MAX_REQUESTS:
        print(f"Blocking IP {ip} due to too many requests.")
        BLOCKED_IPS.add(ip)
        conn.close()
        continue
    
    data = conn.recv(1024).decode()
    if data:
        print(f"Received from {ip}: {data}")
    
    conn.send(b"Request received")
    conn.close()
