import socket
from collections import defaultdict
import time

connections = defaultdict(int)

def detect_ddos(ip):
    current_time = time.time()
    connections[ip] = [t for t in connections[ip] if t > current_time - 5]
    connections[ip].append(current_time)
    return len(connections[ip]) > 5 

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9000))
    server.listen(5)
    print("DDoS Detection Server is running...")

    while True:
        conn, addr = server.accept()
        ip = addr[0]
        if detect_ddos(ip):
            print(f"Blocking potential attack from {ip}")
            conn.send(b"You are blocked!")
            conn.close()
        else:
            conn.send(b"Connection accepted.")
            conn.close()

if __name__ == "__main__":
    start_server()
