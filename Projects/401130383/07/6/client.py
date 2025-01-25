import socket
import time

def ddos_test_client():
    server_host = 'localhost'
    server_port = 12354
    request_count = int(input("Enter number of requests to send: "))
    interval = float(input("Enter interval between requests (in seconds): "))

    for i in range(request_count):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_host, server_port))
            s.send(b"Request")
            response = s.recv(1024).decode()
            print(f"Response: {response}")
            s.close()
        except:
            print("Error connecting to server.")
        time.sleep(interval)

if __name__ == "__main__":
    ddos_test_client()
