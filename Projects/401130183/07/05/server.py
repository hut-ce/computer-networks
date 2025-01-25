import socket

open_ports = [12345, 12346, 12347]

servers = []
for port in open_ports:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(1)
    servers.append(server)

print("Server is running. Open ports:", open_ports)
input("Press Enter to stop the server...")
for server in servers:
    server.close()
