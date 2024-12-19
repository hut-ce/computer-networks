import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5050))

name = socket.gethostname()
client.send(name.encode('utf-8'))

numbers = []


def receive_message(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Connection lost!")
            break


thread = threading.Thread(target=receive_message, args=(client,))
thread.start()

try:
    while True:
        num = input("Enter a number: ")
        if num == '0':
            client.send((", ".join(str(x) for x in numbers)).encode('utf-8'))
            print('list has sent to the server!\n')
            numbers.clear()
        else:
            numbers.append(int(num))


except KeyboardInterrupt:
    print("Connection is getting closed.")
    client.close()
