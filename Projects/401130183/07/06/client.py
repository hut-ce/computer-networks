import socket
import time

target_ip = "127.0.0.1"
target_port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_ip, target_port))

for _ in range(20):
    client.send(b"Hello, server")
    response = client.recv(1024).decode()
    print("Server response:", response)
    time.sleep(0.1)

client.close()
