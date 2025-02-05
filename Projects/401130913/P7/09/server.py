import socket

assigned_ips = {}
ip_pool = ["192.168.1.100", "192.168.1.101", "192.168.1.102"]

def start_dhcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", 12000))
    print("DHCP Server is running...")

    while True:
        data, addr = server.recvfrom(1024)
        if addr not in assigned_ips:
            assigned_ips[addr] = ip_pool.pop(0) if ip_pool else "No IP available"
        server.sendto(assigned_ips[addr].encode(), addr)

if __name__ == "__main__":
    start_dhcp_server()
