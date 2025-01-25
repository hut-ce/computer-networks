import random
import socket
import time
import threading

class DHCPServer:
    def init(self, ip_pool_start, ip_pool_end):
        self.ip_pool = [f"192.168.1.{i}" for i in range(ip_pool_start, ip_pool_end + 1)]
        self.allocated_ips = set()
        self.server_ip = "192.168.1.1"
        self.port = 67 
        self.running = True

    def allocate_ip(self):
        available_ips = list(set(self.ip_pool) - self.allocated_ips)
        if available_ips:
            ip = random.choice(available_ips)
            self.allocated_ips.add(ip)
            return ip
        else:
            return None

    def release_ip(self, ip):
        if ip in self.allocated_ips:
            self.allocated_ips.remove(ip)

    def handle_client(self, client_socket, client_address):
        print(f"Client {client_address} connected.")
        
        print("Sending DHCPOFFER...")
        offered_ip = self.allocate_ip()
        
        if offered_ip:
            client_socket.sendto(f"DHCPOFFER {offered_ip}".encode(), client_address)
            print(f"Offered IP: {offered_ip}")

            # Request
            request_data, _ = client_socket.recvfrom(1024)
            if request_data.decode().startswith("DHCPREQUEST"):
                print(f"Client requested IP: {offered_ip}")
                client_socket.sendto(f"DHCPACK {offered_ip}".encode(), client_address)
                print(f"Acknowledged IP: {offered_ip}")
        else:
            print("No IP available.")
        
        client_socket.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.server_ip, self.port))
        print("DHCP Server is running...")

        while self.running:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    dhcp_server = DHCPServer(2, 254)  
    dhcp_server.start()
