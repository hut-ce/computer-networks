import socket
import threading

clients = {}
block_list = {}
def handle_client(conn, addr):
    username = conn.recv(1024).decode('utf-8')
    print(username + " connected!")
    clients[username] = conn
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if msg.startswith("/pm "):  # Private message
                parts = msg.split(" ", 2)
                if len(parts) > 2:
                    target_user = parts[1]
                    if target_user in block_list.get(username, []):
                        conn.send("You can't message someone you've blocked.".encode('utf-8'))
                    elif username in block_list.get(target_user, []):
                        conn.send((target_user + " has blocked you.").encode('utf-8'))
                    else:
                        private_msg = f"(Private from {username}): {parts[2]}"
                        clients[target_user].send(private_msg.encode('utf-8'))
                else:
                    conn.send("Wrong format! Example: /pm user message".encode('utf-8'))
            elif msg.startswith("/block "):
                parts = msg.split(" ", 1)
                if len(parts) > 1:
                    block_user = parts[1]
                    if username not in block_list:
                        block_list[username] = []
                    block_list[username].append(block_user)
                    conn.send((block_user + " blocked successfully.").encode('utf-8'))
                else:
                    conn.send("Wrong format. Example: /block username".encode('utf-8'))
            elif msg.startswith("/unblock "):
                parts = msg.split(" ", 1)
                if len(parts) > 1:
                    unblock_user = parts[1]
                    if unblock_user in block_list.get(username, []):
                        block_list[username].remove(unblock_user)
                        conn.send((unblock_user + " unblocked successfully.").encode('utf-8'))
                    else:
                        conn.send((unblock_user + " is not in your block list.").encode('utf-8'))
                else:
                    conn.send("Wrong format! Example: /unblock username".encode('utf-8'))
            else:
                broadcast_msg = f"{username}: {msg}"
                for user, client_conn in clients.items():
                    if user != username:
                        client_conn.send(broadcast_msg.encode('utf-8'))
        except:
            print(username + " disconnected.")
            clients.pop(username, None)
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
    main()
