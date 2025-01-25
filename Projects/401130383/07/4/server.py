import socket
import threading
import json


def load_data():
    try:
        with open('data_store.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_data():
    with open('data_store.json', 'w') as file:
        json.dump(data_store, file)


data_store = load_data()


def handle_client(client_socket):
    with client_socket:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            command, *args = request.split()

            if command == 'GET':
                key = args[0]
                response = data_store.get(key, 'Key not found')
            elif command == 'SET':
                key, value = args
                data_store[key] = value
                save_data()
                response = f'{key} set to {value}'
            elif command == 'DELETE':
                key = args[0]
                response = data_store.pop(key, 'Key not found')
                save_data()
            else:
                response = 'Invalid command'

            client_socket.send(response.encode('utf-8'))


def server(host='127.0.0.1', port=8020):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f'Server running on {host}:{port}')
    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == '__main__':
    server()
