import socket

def dhcp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Use UDP
    client_socket.settimeout(5)
    server_address = ('localhost', 12357)

    try:
        # DISCOVER
        print("Sending DISCOVER...")
        client_socket.sendto(b"DISCOVER", server_address)

        # Receive OFFER
        message, _ = client_socket.recvfrom(1024)
        message = message.decode()
        if message.startswith("OFFER"):
            offered_ip = message.split()[1]
            print(f"Received OFFER: {offered_ip}")

            # REQUEST
            print(f"Requesting IP: {offered_ip}")
            client_socket.sendto(f"REQUEST {offered_ip}".encode(), server_address)

            # Receive ACK/NAK
            message, _ = client_socket.recvfrom(1024)
            message = message.decode()
            if message.startswith("ACK"):
                assigned_ip = message.split()[1]
                print(f"IP Address assigned: {assigned_ip}")
            else:
                print("IP request denied.")
        else:
            print("No OFFER received.")
    except socket.timeout:
        print("DHCP server not responding.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    dhcp_client()
