import socket
import threading

bad_words = ["badword1", "badword2"]
shift = 1  

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

def filter_message(message):
    for word in bad_words:
        if word in message:
            return False
    return True

def handle_client(client_socket, client_address):
    print(f"{client_address} connected.")
    username = f"user{len(clients) + 1}"
    blocked_users[username] = set()  
    clients.append((client_socket, username))

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'exit':
                print(f"{client_address} disconnected.")
                break
            
         
            decrypted_message = caesar_decipher(message, shift)

            if decrypted_message.startswith('/block'):
                _, user_to_block = decrypted_message.split(' ', 1)
                blocked_users[username].add(user_to_block)
                client_socket.send(f"{user_to_block} blocked.".encode('utf-8'))
            elif decrypted_message.startswith('/private'):
                _, recipient, private_message = decrypted_message.split(' ', 2)
                send_private_message(recipient, private_message, username, client_socket)
            else:
                broadcast(decrypted_message, client_socket)
        except:
            break

    client_socket.close()
    clients.remove((client_socket, username))
    del blocked_users[username]

def send_private_message(recipient, message, sender_username, sender_socket):
    if filter_message(message):
        if recipient in blocked_users[sender_username]:
            sender_socket.send(f"شما نمی‌توانید به {recipient} پیام ارسال کنید.".encode('utf-8'))
            return
        
        for client in clients:
            if client[1] == recipient:
                client[0].send(f"[پیام خصوصی از {sender_username}: {message}]".encode('utf-8'))
                return
    else:
        sender_socket.send("پيام حاوي کلمات نامناسب است.".encode('utf-8'))

def broadcast(message, sender_socket):
    for client in clients:
        if client[0] != sender_socket:
            client[0].send(message.encode('utf-8'))

blocked_users = {}

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((local_ip, 9999))  
server.listen(5)
clients = []

print(f"server listning {local_ip}...")

while True:
    client_socket, client_address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()
