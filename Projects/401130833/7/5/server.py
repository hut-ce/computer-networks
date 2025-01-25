import socket

def setup_server_ports():
    # Create multiple server sockets to simulate open ports
    sockets = []
    for port in range(12350, 12353):  # Example: Ports 12350, 12351, 12352
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', port))
        s.listen(1)
        sockets.append(s)
        print(f"Server listening on port {port}")
    return sockets

def port_scan_server():
    # Set up server sockets to simulate open ports
    server_sockets = setup_server_ports()
    try:
        print("Server is ready for port scanning simulation.")
        while True:
            pass  # Server doesn't close until interrupted
    except KeyboardInterrupt:
        print("Shutting down servers...")
    finally:
        for s in server_sockets:
            s.close()

if __name__ == "__main__":
    port_scan_server()
