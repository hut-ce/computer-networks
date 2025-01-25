import socket

# Dictionary to store key-value pairs
store = {}

def process_request(request):
    try:
        parts = request.split()
        command = parts[0].upper()
        if command == "SET":
            key, value = parts[1], parts[2]
            store[key] = value
            return f"Key '{key}' set to '{value}'."
        elif command == "GET":
            key = parts[1]
            return store.get(key, f"Key '{key}' not found.")
        else:
            return "Invalid command. Use SET or GET."
    except IndexError:
        return "Invalid command format."

def key_value_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12348))
    server_socket.listen(1)
    print("Key-Value Server is listening...")
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    while True:
        request = conn.recv(1024).decode()
        if not request or request.lower() == 'exit':
            print("Closing connection...")
            break
        response = process_request(request)
        conn.send(response.encode())
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    key_value_server()
