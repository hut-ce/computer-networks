import socket
import threading
from collections import defaultdict

MAX_REQUESTS = 10  
BLOCK_TIME = 60    

request_count = defaultdict(int)
blocked_ips = set()  
def handle_client(client_socket, addr):
    """مدیریت ارتباط با کلاینت"""
    global request_count, blocked_ips

    if addr[0] in blocked_ips:
        print(f"IP {addr[0]} blocked.")
        client_socket.close()
        return

    # افزایش تعداد درخواست‌ها
    request_count[addr[0]] += 1
    print(f"IP {addr[0]}: num request {request_count[addr[0]]}")

    if request_count[addr[0]] > MAX_REQUESTS:
        print(f"IP {addr[0]} بیش از حد مجاز درخواست ارسال کرده است. مسدود می‌شود.")
        blocked_ips.add(addr[0])
        client_socket.close()
        return

    response = "درخواست شما دریافت شد."
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())  
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"server {host}:{port} listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"new connected {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
