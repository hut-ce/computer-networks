import socket
import struct
import time

class DHCPClient:
    def __init__(self, server_ip):
        self.server_ip = server_ip

    def send_dhcp_discover(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client_socket.settimeout(5)

        discover_packet = struct.pack("!4s4s4s4s", b'\x01', b'\x00', b'\x00', b'\x00')

        client_socket.sendto(discover_packet, ('<broadcast>', 67))
        print("Sent DHCP Discover...")
        try:
            offer_packet, server_addr = client_socket.recvfrom(1024)
            print(f"Received DHCP Offer from {server_addr}")
            return offer_packet
        except socket.timeout:
            print("Timeout waiting for Offer.")
            return None

    def send_dhcp_request(self, offer_packet):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        request_packet = struct.pack("!4s4s4s4s", offer_packet[4:8], b'\x00', b'\x00', b'\x00')
        client_socket.sendto(request_packet, (self.server_ip, 67))
        print("Sent DHCP Request...")
        ack_packet, _ = client_socket.recvfrom(1024)
        print(f"Received DHCP Acknowledgement: {ack_packet}")

    def start(self):
        offer_packet = self.send_dhcp_discover()
        if offer_packet:
            self.send_dhcp_request(offer_packet)

dhcp_client = DHCPClient('192.168.1.1')
dhcp_client.start()
