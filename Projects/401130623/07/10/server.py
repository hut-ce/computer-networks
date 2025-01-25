import socket
import threading
from queue import Queue
queue = Queue() 

def board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)
def check_winner(board, player):
    for row in board:
        if row.count(player) == 3:
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False
def handle_game(player1_socket, player2_socket):
    board = [[" " for _ in range(3)] for _ in range(3)]  
    current_player = 'X'
    while True:
        player_socket = player1_socket if current_player == 'X' else player2_socket
        player_socket.send(f"Now its your turn. Current board:\n".encode('utf-8'))
        board(board)
        move = player_socket.recv(1024).decode()
        row, col = map(int, move.split(","))
        if board[row][col] == " ":
            board[row][col] = current_player
            if check_winner(board, current_player):
                player_socket.send(f"Woww! {current_player} wins!\n".encode('utf-8'))
                if current_player == 'X':
                    player2_socket.send(f"Game Over! {current_player} wins!\n".encode('utf-8'))
                else:
                    player1_socket.send(f"Game Over! {current_player} wins!\n".encode('utf-8'))
                board(board)
                break
            current_player = 'O' if current_player == 'X' else 'X'
        else:
            player_socket.send("Invalid move, try again.".encode('utf-8'))

def handle_client(client_socket, client_address):
    print(f"new client {client_address} connected.")
    if queue.qsize() >= 2:
        print("new game")
        player1 = queue.get()
        player2 = queue.get()
        threading.Thread(target=handle_game, args=(player1, player2)).start()
    queue.put(client_socket)  
    print(f"{client_address} added")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 45))
    server_socket.listen(5)
    print("Server is listening on 127.0.0.1:45")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
