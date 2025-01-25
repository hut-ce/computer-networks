import socket
import random

ip_pool = [f"192.168.1.{i}" for i in range(100, 201)]
allocated_ips = {}

def dhcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12357))
    print("DHCP Server is listening...")

    while True:
        message, client_addr = server_socket.recvfrom(1024)
        message = message.decode()

        if message == "DISCOVER":
            print(f"DISCOVER received from {client_addr}")
            offered_ip = random.choice(ip_pool)
            server_socket.sendto(f"OFFER {offered_ip}".encode(), client_addr)
        
        elif message.startswith("REQUEST"):
            _, requested_ip = message.split()
            if requested_ip in ip_pool and requested_ip not in allocated_ips.values():
                allocated_ips[client_addr] = requested_ip
                server_socket.sendto(f"ACK {requested_ip}".encode(), client_addr)
                print(f"Assigned IP {requested_ip} to {client_addr}")
            else:
                server_socket.sendto(b"NAK", client_addr)
                print(f"Request for IP {requested_ip} denied.")

if __name__ == "__main__":
    dhcp_server()
