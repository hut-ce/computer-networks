import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 34))
    print("Connected to the server.")
    try:
        client_socket.send("DHCP_DISCOVER".encode('utf-8'))
        print("Sent DHCP.")
        offer_message = client_socket.recv(1024).decode('utf-8')
        if offer_message.startswith("DHCP_OFFER"):
            offered_ip = offer_message.split(" ")[1]
            print(f"Received IP offer: {offered_ip}")
            client_socket.send(f"DHCP_REQUEST {offered_ip}".encode('utf-8'))
            print(f"Sent request for ip: {offered_ip}")     
            ack_message = client_socket.recv(1024).decode('utf-8')
            if ack_message.startswith("DHCP_ACK"):
                allocated_ip = ack_message.split(" ")[1]
                print(f"ip : {allocated_ip}")
            else:
                print(f"NAK : {ack_message}")
        else:
            print("No ip offered.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print("Disconnected from DHCP server.")

if __name__ == "__main__":
    main()
