import socket
import threading
import time
import requests
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
def get():
    try:
        response = requests.get(API_URL)
        data = response.json()
        rates = {
            "USD": data["rates"]["USD"],
            "EUR": data["rates"]["EUR"],
            "JPY": data["rates"]["JPY"]
        }
        return rates
    except Exception as error:
        print("Error fetching exchange rates:", error)
        return {}

def send(clients):
    while True:
        rates = get()
        if rates:
            message = f"USD: {rates['USD']}, EUR: {rates['EUR']}, JPY: {rates['JPY']}"
            for client in clients:
                try:
                    client.sendall(message.encode('utf-8'))
                except:
                    clients.remove(client)  
        time.sleep(2)  

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

def main():
    clients = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12))
    server.listen(5)
    print("Server is listening on 127.0.0.1:12")
    threading.Thread(target=send, args=(clients,), daemon=True).start()
    while True:
        client_socket, _ = server.accept()
        print("New client connected")
        threading.Thread(target=handle_client, args=(client_socket, clients), daemon=True).start()

if __name__ == "__main__":
    main()
