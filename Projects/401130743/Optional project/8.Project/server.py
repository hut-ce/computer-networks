import socket
import threading


dnses = {
    "google.com": "142.250.74.78",
    "youtube.com": "142.250.74.174",
    "facebook.com": "157.240.22.35",
    "twitter.com": "104.244.42.1",
    "instagram.com": "185.60.216.35",
    "wikipedia.org": "208.80.154.224",
    "amazon.com": "205.251.242.103",
    "linkedin.com": "108.174.10.10",
    "netflix.com": "52.18.174.87",
    "apple.com": "17.253.144.10"
}


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5353))  
    server_socket.listen(5)
    print("[SERVER] DNS Server is running on port 5353...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    try:
        while True:
            
            domain_name = client_socket.recv(1024).decode()
            if not domain_name:
                break
            
            print(f"[REQUEST] Domain requested: {domain_name}")
            
            
            ip_address = dnses.get(domain_name, "Domain not found")
            client_socket.send(ip_address.encode())
    except:
        print(f"[ERROR] Issue with client {client_address}")
    finally:
        print(f"[DISCONNECT] {client_address} disconnected.")
        client_socket.close()


if __name__ == "__main__":
    start_server()
