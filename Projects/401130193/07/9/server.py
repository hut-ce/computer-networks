import socket
import random

ip_address_pool = [f"192.168.1.{i}" for i in range(100, 201)]
leased_ips = {}


def handle_request(sock, client_address, data):
    if data == "DISCOVER":
        print(f"DISCOVER received from {client_address}")
        ip_offer = random.choice(ip_address_pool)
        sock.sendto(f"OFFER {ip_offer}".encode(), client_address)

    elif data.startswith("REQUEST"):
        _, desired_ip = data.split()
        if desired_ip in ip_address_pool and desired_ip not in leased_ips.values():
            leased_ips[client_address] = desired_ip
            sock.sendto(f"ACK {desired_ip}".encode(), client_address)
            print(f"Allocated IP {desired_ip} to {client_address}")
        else:
            sock.sendto(b"NAK", client_address)
            print(f"IP request for {desired_ip} denied.")


def server_dhcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 12357))
    print("DHCP Server is active and waiting for requests...")

    while True:
        data, client_address = sock.recvfrom(1024)
        data = data.decode()
        handle_request(sock, client_address, data)


if __name__ == "__main__":
    server_dhcp()
