import socket
import time

def send_requests_to_server():
    target_host = 'localhost'
    target_port = 12354
    num_requests = int(input("How many requests would you like to send? "))
    delay = float(input("Enter delay between requests (seconds): "))

    for _ in range(num_requests):
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((target_host, target_port))
            connection.send(b"Request")
            reply = connection.recv(1024).decode()
            print(f"Server reply: {reply}")
            connection.close()
        except Exception as e:
            print(f"Connection error: {e}")
        time.sleep(delay)

if __name__ == "__main__":
    send_requests_to_server()
