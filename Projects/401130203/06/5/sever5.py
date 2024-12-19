import socket
import threading

clients = {}
roles = {}
def handle_client(conn, addr):
    username = conn.recv(1024).decode('utf-8')
    print(username + " connected!")
    clients[username] = conn
    if username not in roles:
        roles[username] = "user"
    conn.send(f"Welcome, {username}! Your role is: {roles[username]}".encode('utf-8'))

    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if msg.startswith("/role "):  # Change role (admin only)
                if roles[username] == "admin":
                    parts = msg.split(" ", 2)
                    if len(parts) > 2:
                        target_user, new_role = parts[1], parts[2]
                        if target_user in roles:
                            roles[target_user] = new_role
                            conn.send(f"{target_user} is now a {new_role}".encode('utf-8'))
                            clients[target_user].send(f"Your role has been changed to {new_role}".encode('utf-8'))
                        else:
                            conn.send(f"User {target_user} not found.".encode('utf-8'))
                    else:
                        conn.send("Wrong format! Example: /role username role".encode('utf-8'))
                else:
                    conn.send("You don't have permission to change roles.".encode('utf-8'))

            elif msg.startswith("/kick "):
                if roles[username] == "admin":
                    parts = msg.split(" ", 1)
                    if len(parts) > 1:
                        target_user = parts[1]
                        if target_user in clients:
                            clients[target_user].send("You have been kicked out by the admin.".encode('utf-8'))
                            clients[target_user].close()
                            clients.pop(target_user, None)
                            roles.pop(target_user, None)
                            conn.send(f"{target_user} has been kicked.".encode('utf-8'))
                        else:
                            conn.send(f"User {target_user} not found.".encode('utf-8'))
                    else:
                        conn.send("Wrong format! Example: /kick username".encode('utf-8'))
                else:
                    conn.send("You don't have permission to kick users.".encode('utf-8'))

            elif msg.startswith("/mute "):
                if roles[username] in ["admin", "moderator"]:
                    parts = msg.split(" ", 1)
                    if len(parts) > 1:
                        target_user = parts[1]
                        if target_user in clients:
                            roles[target_user] = "muted"
                            conn.send(f"{target_user} has been muted.".encode('utf-8'))
                            clients[target_user].send("You have been muted.".encode('utf-8'))
                        else:
                            conn.send(f"User {target_user} not found.".encode('utf-8'))
                    else:
                        conn.send("Wrong format! Example: /mute username".encode('utf-8'))
                else:
                    conn.send("You don't have permission to mute users.".encode('utf-8'))

            elif roles[username] == "muted":
                conn.send("You are muted and cannot send messages.".encode('utf-8'))

            else:
                broadcast_msg = f"{username}: {msg}"
                for user, client_conn in clients.items():
                    if user != username:
                        client_conn.send(broadcast_msg.encode('utf-8'))

        except:
            print(username + " disconnected.")
            clients.pop(username, None)
            roles.pop(username, None)
            break
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5050))
    server.listen()
    print("Server is running...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    roles["admin"] = "admin"  # Predefine an admin user for testing
    main()
