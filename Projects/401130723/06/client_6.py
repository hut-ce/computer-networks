import socket
import threading

nickname = input("Choose your nickname: ")

ip = socket . gethostbyname(socket.gethostname())
port = 5050
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip , port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(f"{message}  ")
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()