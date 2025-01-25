import socket
import threading

dns = {
    "france.com": "324.754.33.67",
    "iran.ir": "468.853.43.568",
    "usa.com": "157.240.22.35",
    "uk.com": "104.244.42.1",
    "japan.com": "185.60.216.35",
    "china.org": "208.80.154.224",
    "iraq.com": "205.251.242.103",
}

def handle_client(client_socket, client_address):
    print(f"NEW  {client_address} CONNECTION.")
    try:
        while True:
            
            domain_name = client_socket.recv(1024).decode()
            if not domain_name:
                break
            print(f"Domain requeste: {domain_name}")
            
            
            ip_address = dns.get(domain_name, "Domain has beennot found")
            client_socket.send(ip_address.encode())
    except:
        print(f"an Issue with client {client_address}")
    finally:
        print(f"client {client_address} disconnected.")
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 113))  
    server_socket.listen(5)
    print("Server is listening 127.0.0.1:113")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
