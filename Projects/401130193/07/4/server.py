import socket
import threading
import json


def load_database():
    """Load data from JSON file or initialize an empty dictionary."""
    try:
        with open('database.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_database():
    """Save current data to the JSON file."""
    with open('database.json', 'w') as file:
        json.dump(database, file, indent=4)


# Shared data dictionary
database = load_database()


def process_client(client_connection):
    """Handle commands from the connected client."""
    with client_connection:
        while True:
            try:
                request = client_connection.recv(1024).decode('utf-8')
                if not request:
                    break

                command_parts = request.split()
                command = command_parts[0].upper()
                args = command_parts[1:]

                if command == 'GET':
                    key = args[0]
                    response = database.get(key, 'Error: Key not found')
                elif command == 'SET':
                    key, value = args
                    database[key] = value
                    save_database()
                    response = f'Success: {key} stored with value {value}'
                elif command == 'REMOVE':
                    key = args[0]
                    response = database.pop(key, 'Error: Key not found')
                    save_database()
                else:
                    response = 'Error: Unsupported command'

                client_connection.send(response.encode('utf-8'))
            except Exception as e:
                print(f"Error while processing client: {e}")
                break


def start_server(host='127.0.0.1', port=5000):
    """Start the key-value server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server is running at {host}:{port}")

        while True:
            client_connection, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")
            threading.Thread(target=process_client, args=(client_connection,)).start()


if __name__ == '__main__':
    start_server()
