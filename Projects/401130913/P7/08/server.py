import socket

dns_records = {
    "google.com": "8.8.8.8",
    "openai.com": "23.96.52.53",
    "example.com": "93.184.216.34"
}

def start_dns_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", 11000))
    print("DNS Server is running...")

    while True:
        data, addr = server.recvfrom(1024)
        domain = data.decode()
        ip = dns_records.get(domain, "Domain not found")
        server.sendto(ip.encode(), addr)

if __name__ == "__main__":
    start_dns_server()
