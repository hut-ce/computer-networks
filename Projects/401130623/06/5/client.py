import socket
import threading

def caesar_cipher_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_char = chr((ord(char.lower()) - ord('a') + shift) % 26 + ord('a'))
            result += shift_char.upper() if char.isupper() else shift_char
        else:
            result += char
    return result

def caesar_cipher_decrypt(text, shift):
    return caesar_cipher_encrypt(text, -shift)

def receive_messages(client_socket, shift):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(caesar_cipher_decrypt(message, shift))
        except Exception as e:
            print(f"Error: {e}")
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 10000))

name = input("Enter your name: ")
role = input("Enter your role (admin, moderator, user): ")

client_socket.send(name.encode('utf-8'))
client_socket.send(role.encode('utf-8'))

shift = 3  

threading.Thread(target=receive_messages, args=(client_socket, shift)).start()

while True:
    message = input()
    if message.lower() == 'exit':
        break
    encrypted_message = caesar_cipher_encrypt(message, shift)
    client_socket.send(encrypted_message.encode('utf-8'))

client_socket.close()
