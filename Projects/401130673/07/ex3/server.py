import socket
import threading
import time
import random

prices = {
    "USD": 1.0,
    "EUR": 0.85,
    "JPY": 110.0
}

def update_prices():
    while True:
        prices["USD"] += random.uniform(-0.01, 0.01)
        prices["EUR"] += random.uniform(-0.01, 0.01)
        prices["JPY"] += random.uniform(-0.5, 0.5)
        time.sleep(5) 

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        response = f"USD: {prices['USD']:.2f}, EUR: {prices['EUR']:.2f}, JPY: {prices['JPY']:.2f}"
        client_socket.send(response.encode('utf-8'))
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5050))
    server.listen(5)
    print("Server started on port 5050")
    threading.Thread(target=update_prices).start()
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
