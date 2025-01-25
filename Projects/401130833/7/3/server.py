import socket
import time
import random

# Generate random currency prices for demonstration
def get_currency_prices():
    return {
        "USD": round(random.uniform(1.0, 1.5), 2),
        "EUR": round(random.uniform(0.9, 1.2), 2),
        "BTC": round(random.uniform(15000, 25000), 2),
    }

def currency_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12347))
    server_socket.listen(1)
    print("Currency Server is listening...")
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    while True:
        request = conn.recv(1024).decode()
        if not request or request.lower() == 'exit':
            print("Closing connection...")
            break
        prices = get_currency_prices()
        response = "\n".join([f"{currency}: {price}" for currency, price in prices.items()])
        conn.send(response.encode())
        time.sleep(1)  # Simulate real-time updates
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    currency_server()
