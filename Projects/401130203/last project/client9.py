import socket
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 67
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto("DISCOVER".encode('utf-8'), (SERVER_HOST, SERVER_PORT))
data, _ = client_socket.recvfrom(1024)
message = data.decode('utf-8')

if message.startswith("OFFER"):
    offered_ip = message.split(" ")[1]
    print(f"Received OFFER: {offered_ip}")

    request_message = f"REQUEST {offered_ip}"
    client_socket.sendto(request_message.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
    data, _ = client_socket.recvfrom(1024)
    ack_message = data.decode('utf-8')

    if ack_message.startswith("ACK"):
        assigned_ip = ack_message.split(" ")[1]
        print(f"Assigned IP: {assigned_ip}")
    else:
        print("Failed to get ACK from server.")
else:
    print("Failed to receive OFFER from server.")

client_socket.close()
