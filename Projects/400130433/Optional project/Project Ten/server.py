import socket
import threading
from queue import Queue


PORT = 5555
HOST = '127.0.0.1'
MAX_PLAYERS = 2  
queue = Queue()  


def print_board(board):
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
        player_socket.send(f"Your turn! Current board:\n".encode())
        print_board(board)

        
        move = player_socket.recv(1024).decode()
        row, col = map(int, move.split(","))
        
        
        if board[row][col] == " ":
            board[row][col] = current_player
            if check_winner(board, current_player):
                player_socket.send(f"Congratulations! {current_player} wins!\n".encode())
                if current_player == 'X':
                    player2_socket.send(f"Game Over! {current_player} wins!\n".encode())
                else:
                    player1_socket.send(f"Game Over! {current_player} wins!\n".encode())
                print_board(board)
                break
            current_player = 'O' if current_player == 'X' else 'X'
        else:
            player_socket.send("Invalid move, try again.".encode())


def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    if queue.qsize() >= MAX_PLAYERS:
        print("[INFO] Starting a new game.")
        player1 = queue.get()
        player2 = queue.get()
        threading.Thread(target=handle_game, args=(player1, player2)).start()
    
    queue.put(client_socket)  
    print(f"[INFO] Player {client_address} added to the queue.")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("[SERVER] Server started on port", PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
