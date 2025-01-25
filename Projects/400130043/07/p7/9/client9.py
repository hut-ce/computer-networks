import socket
import time

class DHCPClient:
    def init(self, server_ip):
        self.server_ip = server_ip
        self.port = 67
        self.ip = None

    def discover(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        print("Sending DHCPDISCOVER...")
        client_socket.sendto(b"DHCPDISCOVER", ("255.255.255.255", self.port))

        offer_data, _ = client_socket.recvfrom(1024)
        offered_ip = offer_data.decode().split()[1]
        print(f"Received DHCPOFFER: {offered_ip}")

        print(f"Sending DHCPREQUEST for IP: {offered_ip}")
        client_socket.sendto(f"DHCPREQUEST {offered_ip}".encode(), (self.server_ip, self.port))

        ack_data, _ = client_socket.recvfrom(1024)
        if ack_data.decode().startswith("DHCPACK"):
            self.ip = offered_ip
            print(f"IP Acknowledged: {self.ip}")

    def release(self):
        if self.ip:
            print(f"Releasing IP: {self.ip}")
            self.ip = None

if __name__ == "__main__":
    dhcp_client = DHCPClient("192.168.1.1")  
    dhcp_client.discover()
    time.sleep(5) 
    dhcp_client.release()
