import socket
import threading


def caesar_cipher(text, shift, decode=False):
    if decode:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "Private message incoming...":
                encrypted_message = client_socket.recv(1024).decode()
                shift = int(input("Enter shift to decode the private message: "))
                print(f"Decoded message: {caesar_cipher(encrypted_message, shift, decode=True)}")
            else:
                print(message)
        except ConnectionResetError:
            print("Connection to server lost.")
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    name = input("Enter your name: ")
    client_socket.send(name.encode())

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        command = input("Enter command (send/block/private message/quit): ")
        client_socket.send(command.encode())
        if command == "send":
            message = input("Enter your message: ")
            client_socket.send(message.encode())
        elif command == "block":
            name = input("Enter the name of the user to block: ")
            client_socket.send(name.encode())
        elif command == "private message":
            recipient = input("Enter the recipient's name: ")
            message = input("Enter your private message: ")
            shift = int(input("Enter shift for encryption: "))
            encrypted_message = caesar_cipher(message, shift)
            client_socket.send(recipient.encode())
            client_socket.send(encrypted_message.encode())
        elif command == "quit":
            client_socket.close()
            break


IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

start_client()
