import socket
dns_records = {
    "google.com": "142.250.190.78",
    "youtube.com": "142.250.190.206",
    "facebook.com": "69.63.176.13",
    "twitter.com": "104.244.42.1",
    "instagram.com": "34.117.237.239",
    "wikipedia.org": "208.80.154.224",
    "amazon.com": "205.251.242.103",
    "linkedin.com": "108.174.10.10",
    "netflix.com": "52.94.225.248",
    "github.com": "140.82.113.3",
}
HOST = "127.0.0.1"
PORT = 5353
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"DNS Server started on {HOST}:{PORT}")

while True:
    request, client_address = server_socket.recvfrom(1024)
    domain_name = request.decode('utf-8').strip()
    print(f"Received request for: {domain_name} from {client_address}")
    response = dns_records.get(domain_name, "Domain not found")
    server_socket.sendto(response.encode('utf-8'), client_address)
