import socket

def scan_ports():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8000))

    print(client.recv(1024).decode())
    target_ip = input("Enter target IP: ")
    client.send(target_ip.encode())

    result = client.recv(4096).decode()
    print(result)
    client.close()

if __name__ == "__main__":
    scan_ports()
