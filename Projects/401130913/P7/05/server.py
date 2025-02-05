import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8000))
    server.listen(1)
    print("Port Scanner Server is running...")

    conn, addr = server.accept()
    print(f"Connection from {addr}")

    conn.send(b"Send target IP to scan.")
    target_ip = conn.recv(1024).decode()

    open_ports = []
    for port in range(1, 1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((target_ip, port)) == 0:
            open_ports.append(port)
        s.close()

    result = f"Open ports: {open_ports}" if open_ports else "No open ports found."
    conn.send(result.encode())
    conn.close()

if __name__ == "__main__":
    start_server()
