import socket
import threading


IP_POOL = ["192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5", "192.168.1.6"]
allocated_ips = {}


def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} is attempting to connect.")

    try:
       
        discover_message = client_socket.recv(1024).decode()
        if discover_message == "DHCP_DISCOVER":
            print(f"[DISCOVER] Received from {client_address}")

            
            if IP_POOL:
                offered_ip = IP_POOL.pop(0)  
                allocated_ips[client_address] = offered_ip
                client_socket.send(f"DHCP_OFFER {offered_ip}".encode())
                print(f"[OFFER] Offered {offered_ip} to {client_address}")

            else:
                client_socket.send("DHCP_NAK Pool Empty".encode())
                print(f"[OFFER FAILED] No IPs left for {client_address}")
                client_socket.close()
                return

        
        request_message = client_socket.recv(1024).decode()
        if request_message.startswith("DHCP_REQUEST"):
            requested_ip = request_message.split(" ")[1]
            print(f"[REQUEST] {client_address} requested {requested_ip}")

            
            if allocated_ips.get(client_address) == requested_ip:
                client_socket.send(f"DHCP_ACK {requested_ip}".encode())
                print(f"[ACK] {requested_ip} allocated to {client_address}")
            else:
                client_socket.send("DHCP_NAK Invalid Request".encode())
                print(f"[NAK] Invalid request from {client_address}")

    except Exception as e:
        print(f"[ERROR] {client_address}: {e}")

    finally:
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 67))  
    server_socket.listen(5)
    print("[SERVER] DHCP Server is running on port 67...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
