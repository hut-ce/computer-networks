import pickle
import socket
import time
from threading import Thread
from caesar import caesar_encode, caesar_decode

swear_words = ["badword1", "badword2", "badword3"]


def filter_message(message: str):
    for swear_word in swear_words:
        message = message.replace(swear_word, "***")
    return message


def send_message(client: 'socket.socket'):
    while True:
        mes = input("")
        if mes.startswith("block||"):
            user = mes.split("||", 1)[1]
            client.send(pickle.dumps({"type": "block", "target": user}))
        elif mes.startswith("unblock||"):
            user = mes.split("||", 1)[1]
            client.send(pickle.dumps({"type": "unblock", "target": user}))
        elif "||" in mes:
            user, message = mes.split("||", 1)
            message = filter_message(message)
            message = caesar_encode(message, 7)
            client.send(pickle.dumps({"type": "PV", "target": user, "message": message}))
        else:
            mes = filter_message(mes)
            mes = caesar_encode(mes, 7)
            client.send(pickle.dumps({"type": "normal", "message": mes}))


def receive_message(client: socket.socket):
    while True:
        data = client.recv(1024)
        if data:
            content = pickle.loads(data)
            if isinstance(content, dict):
                message = caesar_decode(content["message"], 7)
                first_key = list(content)[0]
                print(first_key, content[first_key], message)
            else:
                print(content)


server_host = '127.0.0.1'
server_port = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

mes = pickle.dumps(input("Your name:"))
client_socket.send(mes)
print(f"{pickle.loads(client_socket.recv(1024))}")

# print('Type "out" to exit the chat room')
print('"ID||message" for unicast message ')
print('"block||username" to block a user')
print('"unblock||username" to unblock a user')

send = Thread(target=send_message, args=(client_socket,))
receive = Thread(target=receive_message, args=(client_socket,))

send.start()
receive.start()

send.join()
receive.join()
