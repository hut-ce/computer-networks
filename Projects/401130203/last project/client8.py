import socket
HOST = "127.0.0.1"
PORT = 5353
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Simple DNS Client")
print("Type a domain name to get its IP address. Type 'exit' to quit.")
while True:
    domain_name = input("Enter domain: ").strip()
    if domain_name.lower() == "exit":
        break
    client_socket.sendto(domain_name.encode('utf-8'), (HOST, PORT))
    response, _ = client_socket.recvfrom(1024)
    print(f"IP Address: {response.decode('utf-8')}")

# بستن سوکت
client_socket.close()
print("Client exited.")
