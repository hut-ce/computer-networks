import socket

def start_client():
    ip = "127.0.0.1"  
    port = 67         

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    print("[CONNECTED] Connected to DHCP server.")

    try:
        
        client_socket.send("DHCP_DISCOVER".encode())
        print("[DISCOVER] Sent DHCP Discover.")

       
        offer_message = client_socket.recv(1024).decode()
        if offer_message.startswith("DHCP_OFFER"):
            offered_ip = offer_message.split(" ")[1]
            print(f"[OFFER] Received IP offer: {offered_ip}")

           
            client_socket.send(f"DHCP_REQUEST {offered_ip}".encode())
            print(f"[REQUEST] Sent request for IP: {offered_ip}")

            
            ack_message = client_socket.recv(1024).decode()
            if ack_message.startswith("DHCP_ACK"):
                allocated_ip = ack_message.split(" ")[1]
                print(f"[ACK] IP allocated: {allocated_ip}")
            else:
                print(f"[NAK] {ack_message}")
        else:
            print("[NAK] No IP offered.")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print("[DISCONNECTED] Disconnected from DHCP server.")

if __name__ == "__main__":
    start_client()
