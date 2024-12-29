import socket
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def main():
    server_ip = input("enter sever IP: ")
    server_port = 9999

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    while True:
        message = input("enter massage: ")
        if message == 'exit':
            break
        
        encrypted_message = caesar_cipher(message, 1)
        client.send(encrypted_message.encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        print(f"پیام دریافتی: {response}")

    client.close()

if __name__ == "__main__":
    main()
