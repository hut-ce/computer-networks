import socket

def send_requests():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9000))
    response = client.recv(1024).decode()
    print(response)
    client.close()

if __name__ == "__main__":
    for _ in range(7):  
        send_requests()
