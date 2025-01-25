import socket
import threading
IPs = ["127.90.0.12", "127.90.0.13", "127.90.0.14", "127.90.0.15"]
allocated_ips = {}
def handle_client(client_socket, client_address):
    print(f"the client  {client_address} wants to connect.")
    try:
        discover_message = client_socket.recv(1024).decode('utf-8')
        if discover_message == "DHCP_DISCOVER":
            print(f"Received from {client_address}")
            if IPs:
                offered_ip = IPs.pop(0)  
                allocated_ips[client_address] = offered_ip
                client_socket.send(f"DHCP_OFFER {offered_ip}".encode('utf-8'))
                print(f"Offered {offered_ip} to {client_address}")

            else:
                client_socket.send("DHCP_NAK Pool Empty".encode('utf-8'))
                print(f"No IPs left for {client_address}")
                client_socket.close()
                return
        request_message = client_socket.recv(1024).decode('utf-8')
        if request_message.startswith("DHCP_REQUEST"):
            requested_ip = request_message.split(" ")[1]
            print(f"client {client_address} requested {requested_ip}")
            if allocated_ips.get(client_address) == requested_ip:
                client_socket.send(f"DHCP_ACK {requested_ip}".encode('utf-8'))
                print(f"{requested_ip} allocated to {client_address}")
            else:
                client_socket.send("DHCP_NAK Invalid Request".encode('utf-8'))
                print(f"Invalid request from {client_address}")

    except Exception as error:
        print(f"the client {client_address} have the error {error}")
    finally:
        client_socket.close()
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 34))  
    server_socket.listen(5)
    print("Server is listening on 127.0.0.1:34")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
