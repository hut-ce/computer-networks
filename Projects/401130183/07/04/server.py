import socket

database = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(5)

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode()
    parts = request.split(" ", 2)
    command = parts[0].upper()

    if command == "SET" and len(parts) == 3:
        key, value = parts[1], parts[2]
        database[key] = value
        response = f"SET {key} successfully."
    elif command == "GET" and len(parts) == 2:
        key = parts[1]
        response = database.get(key, "Key not found.")
    elif command == "DELETE" and len(parts) == 2:
        key = parts[1]
        if key in database:
            del database[key]
            response = f"Deleted {key} successfully."
        else:
            response = "Key not found."
    else:
        response = "Invalid command. Use SET, GET, or DELETE."

    conn.send(response.encode())
    conn.close()
