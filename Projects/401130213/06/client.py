import socket
import threading


def caesar_cipher_decode(text, shift):
    return caesar_cipher_encode(text, -shift)


def caesar_cipher_encode(text, shift):
    result = ""

    for i in range(len(text)):
        char = text[i]

        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char

    return result


def check_for_profanity(message: str):
    PROFANITY_WORDS = [
        'suck',
        'stupid',
        'pimp',
        'dumb',
        'homo',
        'slut',
        'damn',
        'ass',
        'rape',
        'poop',
        'cock',
        'crap',
        'sex',
        'nazi',
        'neo-nazi',
        'fuck',
        'bitch',
        'pussy',
        'penis',
        'vagina',
        'whore',
        'shit',
        'nigger',
        'nigga',
        'cocksucker',
        'motherfucker',
        'wanker',
        'cunt',
        'faggot',
        'fags',
        'asshole',
        'piss',
        'cum'
    ]
    for i in PROFANITY_WORDS:
        if i in message:
            message = message.replace(i, "***")
    return message


IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP, PORT))

name = input("Please enter your name: ")


def receive_message(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            if message == "quit!!!":
                print("something went wrong!")
                client.close()
                exit()
            if message == "pv incoming":
                pv_message = client.recv(1024).decode()
                shift_amount = input("Incoming private message! Please enter a shift amount to decode the message: ")
                pv_message_decoded = caesar_cipher_decode(pv_message, int(shift_amount))
                print(pv_message_decoded)

            else:
                print(message)
        except ConnectionResetError:
            print("Connection with the server is lost!")
            break
        except ConnectionAbortedError:
            break


thread = threading.Thread(target=receive_message, args=(client,))
thread.start()

try:
    client.send(str(name).encode('utf-8'))
    while True:
        command = input("Please enter your command ('send(s)', 'block(b)', private message(pv), quit(q), login(l), kick(k):\n")
        client.send(str(command).encode('utf-8'))

        if command == "send" or command == "s":
            message = input("Please write your message: \n")
            message = check_for_profanity(message)
            client.send(f"{name} : {message}".encode('utf-8'))
        elif command == "block" or command == "b":
            blocked_name = input("Please enter the nameof whom you want to block...\n")
            client.send(str(blocked_name).encode('utf-8'))

        elif command == "private message" or command == "pv":
            recipient = input("Please enter your recipient name: \n")
            client.send(str(recipient).encode('utf-8'))

            shift_amount = input("Please enter a shift amount for encrypting the text: \n")
            message = input("Please write your message: \n")
            message = check_for_profanity(message)
            encrypted_message = caesar_cipher_encode(f"'Private message'{name} : {message}", int(shift_amount))
            client.send(encrypted_message.encode('utf-8'))

        elif command == "quit" or command == "q":
            client.close()
            exit()

        elif command == "kick" or command == "k":
            recipient = input("Please enter your recipient name: \n")
            client.send(str(recipient).encode('utf-8'))

        elif command == "login" or command == "l":
            username = input("Please enter your Username:")
            password = input("Please enter your Password:")
            client.send(str(username).encode('utf-8'))
            client.send(str(password).encode('utf-8'))

except KeyboardInterrupt:
    print("Connection is getting closed...")
    client.close()
