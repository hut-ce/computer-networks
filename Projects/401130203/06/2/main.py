import socket
import threading
def encrypt_msg(text, key):
    encrypted = ""
    for c in text:
        if c.isalpha():
            shift = key % 26
            if c.islower():
                encrypted += chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
            else:
                encrypted += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        else:
            encrypted += c
    return encrypted
def decrypt_msg(text, key):
    return encrypt_msg(text, -key)

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == "USERNAME":
                client.send(username.encode('utf-8'))
            else:
                decoded_msg = decrypt_msg(msg, key)
                print(decoded_msg)
        except:
            print("error")
            client.close()
            break
def send():
    while True:
        try:
            text = input()
            if text.startswith("/pm "):
                parts = text.split(" ", 2)
                if len(parts) > 2:
                    private_user = parts[1]
                    private_msg = encrypt_msg(parts[2], key)
                    client.send(f"/pm {private_user} {private_msg}".encode('utf-8'))
                else:
                    print("error use this /pm <username> <message>")
            else:
                enc_msg = encrypt_msg(text, key)
                client.send(enc_msg.encode('utf-8'))
        except:
            print("error")
            break
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(("127.0.0.1", 5050))
except:
    print("unsesseful")
    exit()
username = input("enter your name ")
key = int(input("enter password key "))
thread_recv = threading.Thread(target=receive)
thread_recv.start()
thread_send = threading.Thread(target=send)
thread_send.start()
