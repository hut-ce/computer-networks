import socket
HOST = "127.0.0.1"
PORT = 67
ip_pool = ["192.168.1.10", "192.168.1.11", "192.168.1.12", "192.168.1.13"]
assigned_ips = {}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind
((HOST, PORT))
print(f"DHCP Server started on {HOST}:{PORT}")
while True:
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode('utf-8').strip()
    print(f"Received: {message} from {client_address}")

    if message == "DISCOVER":
        ip_offer = ip_pool[0]
        response = f"OFFER {ip_offer}"
        print(f"Offering IP: {ip_offer} to {client_address}")
        server_socket.sendto(response.encode('utf-8'), client_address)

    elif message.startswith("REQUEST"):
        requested_ip = message.split(" ")[1]
        assigned_ips[client_address] = requested_ip
        response = f"ACK {requested_ip}"
        print(f"Assigned IP: {requested_ip} to {client_address}")
        server_socket.sendto(response.encode('utf-8'), client_address)


