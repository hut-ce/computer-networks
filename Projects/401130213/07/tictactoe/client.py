import socket
import threading
import pickle

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

name = input("Please enter your name: ")
client.connect((IP, PORT))


def receive_message(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Connection with the server is lost!")
            break
        except ConnectionAbortedError:
            break


print("waiting for other players...")
data_received = client.recv(10000)
player_number = data_received[:7].decode()
board_data = data_received[7:]
board = pickle.loads(board_data)
print(board)

print(f"you are playing as {player_number}")
if player_number == 'player1':
    player_mark = 'X'
else:
    player_mark = 'O'

try:
    while True:
        board_data = client.recv(10000)
        if board_data == b'you lost!':
            print("you lost!")
            break
        board = pickle.loads(board_data)
        for i in board:
            print(i)
        message = input("make your move (pos_x, pos_y): \n")
        pos_x, pos_y = message.split(",")
        client.send(f"{player_number}:{pos_x},{pos_y}".encode('utf-8'))
    client.close()
except KeyboardInterrupt:
    print("Connection is getting closed...")
    client.close()

