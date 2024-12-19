import socket
import threading

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_char = chr((ord(char.lower()) - ord('a') + shift) % 26 + ord('a'))
            result += shift_char.upper() if char.isupper() else shift_char
        else:
            result += char
    return result

def caesar_cipher_decrypt(text, shift):
    return caesar_cipher(text, -shift)

def receive_messages(client, shift):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(caesar_cipher_decrypt(message, shift))
        except ConnectionResetError:
            print("connection with server is lost")
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5050))

name = input("name: ")
role = input("choose role (admin, moderator, user): ")

client.send(name.encode('utf-8'))
client.send(role.encode('utf-8'))

shift = 3  

thread=threading.Thread(target=receive_messages, args=(client, shift))
thread=thread.start()

try:
    while True:
        message = input("type: \n")
        encrypted_message = caesar_cipher(message, shift)
        client.send(encrypted_message.encode('utf-8'))

except KeyboardInterrupt:
    print("connection is closed.")
    client.close()

