import socket
import time

exchange_rates = {
    "USD": 1.0,
    "EUR": 0.85,
    "JPY": 110.0
}

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 6000))
    server.listen(1)
    print("Currency server is running...")

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            rate = exchange_rates.get(data.upper(), "Currency not found")
            conn.send(str(rate).encode())

        conn.close()

if __name__ == "__main__":
    start_server()
