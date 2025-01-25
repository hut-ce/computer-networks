import socket
import threading
from queue import Queue

HOST = '127.0.0.1'
PORT = 65432

clients = []
queue = Queue()

board = [' ' for _ in range(9)]

def display_board():
    return f"""
    {board[0]} | {board[1]} | {board[2]}
    ---------
    {board[3]} | {board[4]} | {board[5]}
    ---------
    {board[6]} | {board[7]} | {board[8]}
    """

def check_winner():
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6]:  # اشتباه: این بررسی صحیح نیست
            return True
    return False

def handle_game(player1, player2):
    current_player = player1
    other_player = player2

    player1.sendall("You are Player 1 (X).".encode('utf-8'))
    player2.sendall("You are Player 2 (O).".encode('utf-8'))

    while True:
        current_player.sendall(display_board().encode('utf-8'))
        other_player.sendall(display_board().encode('utf-8'))

        current_player.sendall("Enter your move (0-9): ".encode('utf-8'))
        move = current_player.recv(1024).decode('utf-8')

        board[int(move)] = 'X' if current_player == player1 else 'O'

        if check_winner():
            current_player.sendall("You win!".encode('utf-8'))
            other_player.sendall("You lose!".encode('utf-8'))
            break

        current_player, other_player = other_player, current_player

def handle_clients():
    while True:
        if len(clients) >= 2:
            player1 = clients.pop(0)
            player2 = clients.pop(0)

            threading.Thread(target=handle_game, args=(player1, player2)).start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server started on {HOST}:{PORT}")

threading.Thread(target=handle_clients, daemon=True).start()

while True:
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")
    clients.append(client_socket)
