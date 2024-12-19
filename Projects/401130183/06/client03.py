import socket
import threading

host = '127.0.0.1' 
port = 12345

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            decrypted_message = caesar_cipher(message, -2) 
            print(decrypted_message)
        except:
            print("Disconnected from the server.")
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print("Connected to the chat room!")

username = input("Enter your username: ")
client.send(username.encode('utf-8'))

thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()

while True:
    message = input()
    if message.lower() == 'exit':
        client.close()
        break
    elif message.startswith('@'):
        client.send(message.encode('utf-8'))
    else:
        encrypted_message = caesar_cipher(message, 2)  # رمزنگاری پیام با کلید 2
        client.send(encrypted_message.encode('utf-8'))
