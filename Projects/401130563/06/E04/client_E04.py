import socket
import threading

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 55555))


def encrypt_caesar(text, shift=3):
    """Encrypt the text using Caesar Cipher with a shift of 3."""
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result


def decrypt_caesar(text, shift=3):
    """Decrypt the text using Caesar Cipher with a shift of 3."""
    return encrypt_caesar(text, shift=-shift)


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message.startswith('[ENC]'):
                encrypted_message = message[5:]
                decrypted_message = decrypt_caesar(encrypted_message)
                print(decrypted_message)
            elif message == 'NICK':
                client.send(nickname.encode("utf-8"))
            else:
                print(message)
        except Exception as e:
            print('[ERROR] An error occurred:', e)
            client.close()
            break


def write():
    while True:
        message = input("")
        if message.startswith('/block '):
            try:
                parts = message.split(' ', 1)
                blocked_nickname = parts[1]
                client.send(f'/block {blocked_nickname}'.encode('utf-8'))
            except IndexError:
                print('[ERROR] Invalid block command. Use: /block <nickname>')

        elif message.startswith('/pm '):
            try:
                parts = message.split(' ', 2)
                recipient_nickname = parts[1]
                actual_message = parts[2]
                full_message = f'{nickname} (private): {actual_message}'
                encrypted_message = encrypt_caesar(full_message)
                client.send(f'/pm {recipient_nickname} [ENC]{encrypted_message}'.encode("utf-8"))
            except IndexError:
                print('[ERROR] Invalid private message format. Use: /pm <nickname> <message>')

        else:
            full_message = f'{nickname}: {message}'
            encrypted_message = encrypt_caesar(full_message)
            client.send(f'[ENC]{encrypted_message}'.encode("utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
