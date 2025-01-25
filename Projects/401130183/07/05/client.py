import socket

target_ip = "127.0.0.1"
start_port = 12340
end_port = 12350

print(f"Scanning ports on {target_ip} from {start_port} to {end_port}...")
open_ports = []

for port in range(start_port, end_port + 1):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(0.5)
    result = client.connect_ex((target_ip, port))
    if result == 0:
        open_ports.append(port)
    client.close()

if open_ports:
    print("Open ports found:", open_ports)
else:
    print("No open ports found.")
