import socket

def request_ip():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b"Request IP", ("127.0.0.1", 12000))

    ip, _ = client.recvfrom(1024)
    print(f"Assigned IP: {ip.decode()}")
    client.close()

if __name__ == "__main__":
    request_ip()
