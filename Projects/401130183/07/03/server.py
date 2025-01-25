import socket
import time
import random

prices = {"USD": 100.0, "JPY": 150.0, "EUR": 120.0}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(1)

while True:
    conn, addr = server.accept()
    while True:
        try:
            for currency in prices:
                prices[currency] += random.uniform(-0.5, 0.5)
            message = f"USD: {prices['USD']:.2f}, JPY: {prices['JPY']:.2f}, EUR: {prices['EUR']:.2f}"
            conn.send(message.encode())
            time.sleep(2)
        except BrokenPipeError:
            break
    conn.close()
