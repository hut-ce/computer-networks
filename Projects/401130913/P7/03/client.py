import socket

def get_exchange_rate():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 6000))

    while True:
        currency = input("Enter currency code (USD, EUR, JPY) or 'exit': ")
        if currency.lower() == "exit":
            break
        client.send(currency.encode())
        response = client.recv(1024).decode()
        print(f"Exchange rate: {response}")

    client.close()

if __name__ == "__main__":
    get_exchange_rate()
