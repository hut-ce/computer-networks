import socket
import random
import struct

class DHCPServer:
    def __init__(self, ip_pool_start, ip_pool_end):
        self.ip_pool_start = ip_pool_start
        self.ip_pool_end = ip_pool_end
        self.ip_pool = [f"192.168.1.{i}" for i in range(ip_pool_start, ip_pool_end + 1)]
        self.allocated_ips = set()

    def generate_dhcp_offer(self, discover_packet):
        transaction_id = discover_packet[4:8]
        client_ip = "0.0.0.0"
        server_ip = "192.168.1.1"
        offered_ip = self.get_available_ip()

        if offered_ip is None:
            print("No IP available in the pool.")
            return None

        self.allocated_ips.add(offered_ip)

        packet = struct.pack("!4s4s4s4s", transaction_id, client_ip.encode(), server_ip.encode(), offered_ip.encode())
        return packet

    def get_available_ip(self):
        if len(self.ip_pool) == len(self.allocated_ips):
            return None
        available_ips = set(self.ip_pool) - self.allocated_ips
        return random.choice(list(available_ips))

    def handle_dhcp_request(self, request_packet):
        transaction_id = request_packet[4:8]
        client_ip = "0.0.0.0"
        offered_ip = self.allocate_ip()
        server_ip = "192.168.1.1"

        ack_packet = struct.pack("!4s4s4s4s", transaction_id, client_ip.encode(), server_ip.encode(), offered_ip.encode())
        return ack_packet

    def allocate_ip(self):
        return self.ip_pool.pop(0)

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('0.0.0.0', 67))

        print("DHCP Server is running...")
        while True:
            data, client_addr = server_socket.recvfrom(1024)

            if data:
                print(f"Received request from {client_addr}")

                if data[0] == 1:  # Discover packet
                    offer_packet = self.generate_dhcp_offer(data)
                    if offer_packet:
                        server_socket.sendto(offer_packet, client_addr)
                elif data[0] == 3:  # Request packet
                    ack_packet = self.handle_dhcp_request(data)
                    server_socket.sendto(ack_packet, client_addr)

dhcp_server = DHCPServer(ip_pool_start=100, ip_pool_end=199)
dhcp_server.start()
