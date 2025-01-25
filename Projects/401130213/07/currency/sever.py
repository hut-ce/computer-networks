import socket
import requests
import threading
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


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
        time.sleep(10)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print("Server is Running and is waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr[1]} is connected to the server!")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    main()
