import socket
import json

storage = {}

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 7000))
    server.listen(1)
    print("Key-Value server is running...")

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            command = json.loads(data)
            action = command.get("action")
            key = command.get("key")
            value = command.get("value")

            if action == "set":
                storage[key] = value
                conn.send(b"Key set successfully.")
            elif action == "get":
                result = storage.get(key, "Key not found.")
                conn.send(result.encode())
            else:
                conn.send(b"Invalid command.")

        conn.close()

if __name__ == "__main__":
    start_server()
