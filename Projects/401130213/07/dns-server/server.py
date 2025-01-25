import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

dns_records = {
    "google.com": "142.250.72.206",
    "facebook.com": "157.240.22.35",
    "youtube.com": "142.250.72.238",
    "wikipedia.org": "208.80.154.224",
    "amazon.com": "205.251.242.103",
    "twitter.com": "104.244.42.129",
    "instagram.com": "157.240.22.174",
    "linkedin.com": "108.174.10.10",
    "hut.ac.ir": "78.39.212.44",
    "stackoverflow.com": "151.101.1.69"
}


def handle_client_connection(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        response = dns_records.get(request, "Domain name not found")
        client_socket.sendall(response.encode('utf-8'))
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print("Server is Running and is waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr[1]} is connected to the server!")
        handle_client_connection(client_socket)


if __name__ == '__main__':
    main()
