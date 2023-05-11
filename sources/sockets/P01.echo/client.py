import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65000  # The port used by the server
# MSG = bytes("Hello, world", "utf-8")
MSG = b"Hello, world"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(MSG)

data = s.recv(1024)

print(f"Received: {data!r}")
s.close() 