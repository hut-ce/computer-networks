import socket
import requests
import threading
import time


def get_currency_rates():
    source_web_addr = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(source_web_addr)
    rates = response.json()["rates"]

    return {
        "JPY": rates["JPY"],
        "EUR": rates["EUR"],
        "USD": 1.0
    }


def handle_client_connection(client_socket):
    while True:
        rates = get_currency_rates()
        message = f"USD to JPY: {rates['JPY']}, USD to EUR: {rates['EUR']}"
        client_socket.sendall(message.encode('utf-8'))



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 55555))
server_socket.listen()
print('[LISTENING] server is listening...!')

while True:
    client_socket, addr = server_socket.accept()
    print(f"[CONNECTION] connection address: {addr[1]}")
    client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
    client_handler.start()
