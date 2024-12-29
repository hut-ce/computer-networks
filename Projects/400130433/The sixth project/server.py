import socket
import threading


clients = []
clients_names = {}
roles = {}


bad_words = ['fuck', 'airhead', 'bastard']  


def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)


def filter_bad_words(message):
    for word in bad_words:
        if word in message.lower():
            message = message.replace(word, '*' * len(word))  
    return message


def caesar_cipher(message, key):
    result = ""
    for char in message:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result


def handle_client(client_socket):
    client_socket.send("Enter your name: ".encode())
    name = client_socket.recv(1024).decode()
    clients_names[client_socket] = name
    roles[client_socket] = "user"  

    
    client_socket.send("Enter your role (admin/observer/user): ".encode())
    role = client_socket.recv(1024).decode()
    if role in ["admin", "observer", "user"]:
        roles[client_socket] = role
    else:
        roles[client_socket] = "user"

    welcome_message = f"{name} has joined the chat!".encode()
    broadcast(welcome_message, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()

            
            message = filter_bad_words(message)

            
            encrypted_message = caesar_cipher(message, 3)

            if message.startswith("/private"):
               
                recipient_name, private_message = message.split(' ', 1)[1].split(':', 1)
                recipient_found = False
                for client, username in clients_names.items():
                    if username == recipient_name:
                        encrypted_message = caesar_cipher(f"Private message from {name}: {private_message}", 3)
                        client.send(encrypted_message.encode())
                        recipient_found = True
                        break
                if not recipient_found:
                    client_socket.send("User not found.".encode())
            else:
                
                broadcast(encrypted_message.encode(), client_socket)
        except:
            break

    clients.remove(client_socket)
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  
    server_socket.listen(5)

    print("Server is listening on port 12345")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
