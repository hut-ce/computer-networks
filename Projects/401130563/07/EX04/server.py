import socket
import threading

data_store = {}


def handle_client_connection(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        command, key, value = parse_request(request)
        response = process_request(command, key, value)
        client_socket.sendall(response.encode('utf-8'))
    client_socket.close()


def parse_request(request):
    parts = request.split(' ')
    command = parts[0].upper()
    key = parts[1] if len(parts) > 1 else None
    value = parts[2] if len(parts) > 2 else None
    return command, key, value


def process_request(command, key, value):
    global data_store
    if command == 'SET' and key and value:
        data_store[key] = value
        return f"SET {key} = {value}"
    elif command == 'GET' and key:
        return data_store.get(key, 'Key not found')
    elif command == 'DELETE' and key:
        return data_store.pop(key, 'Key not found')
    else:
        return 'Invalid command'


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 55555))
server_socket.listen()
print('[LISTENING] server is listening...!')

while True:
    client_socket, addr = server_socket.accept()
    print(f'[CONNECTION] connection address: {addr[1]}')
    client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
    client_handler.start()
