# client_dhcp.py
import socket

def client_dhcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    server_address = ('localhost', 12357)

    try:
        print("Initiating DISCOVER...")
        sock.sendto(b"DISCOVER", server_address)

        response, _ = sock.recvfrom(1024)
        response = response.decode()
        if response.startswith("OFFER"):
            ip_offer = response.split()[1]
            print(f"Received OFFER for IP: {ip_offer}")

            print(f"Sending REQUEST for IP: {ip_offer}")
            sock.sendto(f"REQUEST {ip_offer}".encode(), server_address)

            response, _ = sock.recvfrom(1024)
            response = response.decode()
            if response.startswith("ACK"):
                ip_assigned = response.split()[1]
                print(f"Assigned IP Address: {ip_assigned}")
            else:
                print("IP request was denied.")
        else:
            print("No valid OFFER received.")
    except socket.timeout:
        print("DHCP server is not responding.")
    finally:
        sock.close()

if __name__ == "__main__":
    client_dhcp()
