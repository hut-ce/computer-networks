import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

while True:
    try:
        data = client.recv(1024).decode()
        print("Current prices:", data)
    except:
        break

client.close()
