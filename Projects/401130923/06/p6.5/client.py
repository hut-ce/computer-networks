import socket
import threading

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - base + shift_amount) % 26 + base)
        else:
            result += char
    return result

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

host = '127.0.0.1'
port = 55555
shift = 1

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

username = input("Enter your username: ")
client.send(username.encode('utf-8'))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message != 'USERNAME':
                print(caesar_decipher(message, shift))
        except:
            print("Error occurred!")
            client.close()
            break

def send_messages():
    while True:
        message = input("")
        if message.startswith('/private') or message.startswith('/block'):
            client.send(message.encode('utf-8'))
        else:
            encrypted_message = caesar_cipher(message, shift)
            client.send(encrypted_message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=send_messages)
write_thread.start()
