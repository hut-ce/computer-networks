import socket
import threading
import time
import requests


Url = "https://api.exchangerate-api.com/v4/latest/USD"


def exchange_rates():
    try:

        response = requests.get(Url)
        data = response.json()
        rates = {
            "USD": data["rates"]["USD"],
            "EUR": data["rates"]["EUR"],
            "JPY": data["rates"]["JPY"]
        }
        return rates
    except Exception as e:
        print("Error fetching exchange rates:", e)
        return {}


def send_prices_to_clients(clients):
    while True:
        rates = exchange_rates()
        if rates:
            message = f"USD: {rates['USD']}, EUR: {rates['EUR']}, JPY: {rates['JPY']}"
            for client in clients:
                try:
                    client.sendall(message.encode())
                except:
                    clients.remove(client)  
        time.sleep(5)  


def handle_client(client_socket, clients):
    clients.append(client_socket)
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
    finally:
        clients.remove(client_socket)
        client_socket.close()


def start_server():
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("Server is listening on port 8080")

    clients = []
    
    
    threading.Thread(target=send_prices_to_clients, args=(clients,), daemon=True).start()

    while True:
        client_socket, _ = server.accept()
        print("New client connected")
        threading.Thread(target=handle_client, args=(client_socket, clients), daemon=True).start()

if __name__ == "__main__":
    start_server()
