import socket
import requests
import time
import threading

def fetch_currency_prices():
    """دریافت قیمت‌های ارز از یک API"""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return {
            "USD": data['rates']['USD'],
            "EUR": data['rates']['EUR'],
            "JPY": data['rates']['JPY']
        }
    except Exception as e:
        print(f"error: {e}")
        return None

def handle_client(client_socket):
    """مدیریت ارتباط با کلاینت"""
    while True:
        prices = fetch_currency_prices()
        if prices:
            message = f"قیمت‌ها: دلار: {prices['USD']}, یورو: {prices['EUR']}, ین: {prices['JPY']}"
            client_socket.send(message.encode())
        time.sleep(5)  

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"server {host}:{port} listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"new connected {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
