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

name = input("Enter your name: ")
client.send(name.encode('utf-8'))

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg != 'NAME':
                decrypted_msg = caesar_decipher(msg, shift)
                print(decrypted_msg)
        except:
            print("Error occurred!")
            client.close()
            break

def send_messages():
    while True:
        try:
            msg = input("")
            encrypted_msg = caesar_cipher(msg, shift)
            client.send(encrypted_msg.encode('utf-8'))
        except:
            print("Error sending message!")
            client.close()
            break

recv_thread = threading.Thread(target=receive_messages)
recv_thread.start()

write_thread = threading.Thread(target=send_messages)
write_thread.start()
