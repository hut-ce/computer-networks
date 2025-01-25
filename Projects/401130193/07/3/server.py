import requests
import socket

def get_crypto_prices():
    api_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple&vs_currencies=usd'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        result = ''
        for coin, info in data.items():
            price = info['usd']
            result += f'{coin.capitalize()}: ${price}\n'
        return result
    except requests.exceptions.RequestException as e:
        print(f'API request error: {e}')
        return "Error fetching data from the API."


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 8010))
        server_socket.listen(5)
        print("Server is running on 127.0.0.1:8010...")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"New client connected: {client_address}")
                try:
                    message = client_socket.recv(1024).decode()
                    if message.lower() == 'prices':
                        client_socket.sendall(get_crypto_prices().encode())
                    else:
                        client_socket.sendall("Invalid request. Send 'prices' to get cryptocurrency rates.".encode())
                except Exception as e:
                    print(f"Error during client communication: {e}")
            print(f"Client disconnected: {client_address}")


if __name__ == '__main__':
    start_server()
