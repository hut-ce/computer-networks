import socket
import random
import time

def start_server(host="127.0.0.1", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server is running... Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print("New connection from", client_address)

        try:
            while True:
                yen = round(random.uniform(100, 150), 2)
                usd = round(random.uniform(1, 2), 2)
                eur = round(random.uniform(0.9, 1.2), 2)
                message = f"Yen: {yen} JPY, USD: {usd} USD, EUR: {eur} EUR"
                client_socket.send(message.encode("utf-8"))
                time.sleep(3)
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()
