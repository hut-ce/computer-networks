import socket
import time

def simulate_client_requests():
    """Simulate multiple requests to test the DDoS protection server."""
    server_host = 'localhost'
    server_port = 12400
    total_requests = int(input("Enter the number of requests to send: "))
    request_delay = float(input("Enter delay between each request (in seconds): "))

    for i in range(total_requests):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_host, server_port))
                client_socket.send(b"Hello Server")
                response = client_socket.recv(1024).decode()
                print(f"[CLIENT] Response from server: {response}")
        except Exception as e:
            print(f"[ERROR] Connection issue: {e}")
        time.sleep(request_delay)

if __name__ == "__main__":
    simulate_client_requests()
