import socket
import threading

dns_table = {
    "google.com": "142.250.72.238",
    "facebook.com": "157.240.229.35",
    "youtube.com": "172.217.18.206",
    "twitter.com": "104.244.42.1",
    "instagram.com": "185.60.218.35",
    "linkedin.com": "108.174.10.10",
    "wikipedia.org": "91.198.174.192",
    "amazon.com": "176.32.103.205",
    "apple.com": "17.253.144.10",
    "microsoft.com": "40.113.200.201"
}

def handle_client(client_socket):
    while True:
        domain = client_socket.recv(1024).decode('utf-8')
        if not domain:
            break
        ip = dns_table.get(domain, "Domain not found")
        client_socket.send(ip.encode('utf-8'))
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 53))  
    server.listen(5)
    print("DNS Server started on port 53")
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
