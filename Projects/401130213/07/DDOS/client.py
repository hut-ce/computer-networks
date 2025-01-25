import socket
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def send_requests(server_ip, port, num_requests):
    for _ in range(num_requests):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((server_ip, port))
            message = client_socket.recv(1024)
            print(message.decode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
        time.sleep(0.1)


def main():
    server_ip = IP
    port = PORT
    num_requests = 150

    send_requests(server_ip, port, num_requests)


if __name__ == '__main__':
    main()
