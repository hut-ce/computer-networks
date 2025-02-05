import socket

def query_dns():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        domain = input("Enter domain to resolve (or 'exit'): ")
        if domain.lower() == "exit":
            break

        client.sendto(domain.encode(), ("127.0.0.1", 11000))
        ip, _ = client.recvfrom(1024)
        print(f"Resolved IP: {ip.decode()}")

    client.close()

if __name__ == "__main__":
    query_dns()
