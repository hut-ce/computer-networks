import requests
import socket


def fetch_exchaing_rates():
    api_url = 'http://api.navasan.tech/latest/?api_key=free93i0OE8hUcVt6W1HSM1TbWKbTQgG'
    try:
        responce = requests.get(api_url)
        responce.raise_for_status()
        data = responce.json()
        responce = ''
        for i in ['usd', 'eur', 'jpy']:
            temp = data[i]
            responce += f'{i}: {temp['value']} - {temp['date']}\n'
        return responce

    except requests.exceptions.RequestException as e:
        print(f'Error request: {e}')
        return None


def server_program():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('127.0.0.1', 8010))
        server.listen()

        while True:
            print('SERVER LISTENING on localhost:8010')
            try:
                client_socket, address = server.accept()
                with client_socket:
                    print(f'CLIENT CONNECTED: {address}')
                    message = client_socket.recv(1024).decode()
                    if message == 'rates':
                        client_socket.sendall(fetch_exchaing_rates().encode())
                    else:
                        client_socket.send('send "rates".'.encode())
                print(f'CLIENT DISCONNECTED: {address}')

            except ConnectionResetError as e:
                print(f'ERROR CONNECTION CLIENT: {e}')

if __name__ == '__main__':
    server_program()