import socket
import threading


bad_words = ["badword1", "badword2"]

def filter_message(message):
    for word in bad_words:
        if word in message:
            return False
    return True

def handle_client(client_socket, client_address):
    print(f"{client_address} connected.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'exit':
                print(f"{client_address} disconnect.")
                break
            
            if message.startswith('/private'):
                _, recipient, private_message = message.split(' ', 2)
                send_private_message(recipient, private_message, client_socket)
            else:
                broadcast(message, client_socket)
        except:
            break

    client_socket.close()

def send_private_message(recipient, message, sender_socket):
    if filter_message(message):
        for client in clients:
            if client[1] == recipient:
                client[0].send(f"[پیام خصوصی از {sender_socket.getpeername()}: {message}]".encode('utf-8'))
                return
    else:
        sender_socket.send("پيام شما حاوي کلمات نامناسب است.".encode('utf-8'))

def broadcast(message, sender_socket):
    for client in clients:
        if client[0] != sender_socket:
            client[0].send(message.encode('utf-8'))

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((local_ip, 9999))  
server.listen(5)
clients = []

print(f"server listtening {local_ip}")

while True:
    client_socket, client_address = server.accept()
    clients.append((client_socket, f"user{len(clients) + 1}"))
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()
