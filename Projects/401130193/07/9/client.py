import socket

def send_request(sock, server_address, message):
    sock.sendto(message.encode(), server_address)
    response, _ = sock.recvfrom(1024)
    return response.decode()

def client_dhcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    server_address = ('localhost', 12357)

    try:
        print("Initiating DISCOVER...")
        discover_response = send_request(sock, server_address, "DISCOVER")

        if discover_response.startswith("OFFER"):
            ip_offer = discover_response.split()[1]
            print(f"Received OFFER for IP: {ip_offer}")

            print(f"Sending REQUEST for IP: {ip_offer}")
            request_response = send_request(sock, server_address, f"REQUEST {ip_offer}")

            if request_response.startswith("ACK"):
                ip_assigned = request_response.split()[1]
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
