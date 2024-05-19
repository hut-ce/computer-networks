import socket
import threading

ip = '127.0.0.10'
port = 5050

clients = []

def handle_client(conn, addr, name):
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"{name}: '{message}'")
                send_for_all_clients(f"{name}: '{message}'")
        except:
            index = clients.index((conn, name))
            clients.remove((conn, name))
            conn.close()
            print(f"{name} disconnected.")
            send_for_all_clients(f"{name} left!")
            break

def send_for_all_clients(message):
    for client in clients:
        client[0].send(message.encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f"Server Running: ({ip}/{port})")

    while True:
        conn, addr = server.accept()
        print(f"New connection: ({addr})")

        conn.send("Type: \n".encode('utf-8'))
        name = conn.recv(1024).decode('utf-8')
        clients.append((conn, name))

        send_for_all_clients(f"{name} joined.")
        # conn.send("You are now connected!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(conn, addr, name))
        thread.start()

start_server()
