import socket
import threading

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 55555))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == 'NICK':
                client.send(nickname.encode("utf-8"))
            else:
                print(message)
        except:
            print('[ERROR] An error occurred')
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode("utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
