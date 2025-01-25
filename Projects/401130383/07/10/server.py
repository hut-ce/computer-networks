import socket
import threading
from queue import Queue

board = [" "] * 9
players = Queue()

def print_board():
    print("\n".join(["|".join(board[i:i+3]) for i in range(0, 9, 3)]))

def check_winner():
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != " ":
            return board[condition[0]]
    return None

def reset_board():
    global board
    board = [" "] * 9

def handle_player(conn, player_symbol):
    while True:
        conn.send(f"BOARD\n{print_board()}".encode())
        move = int(conn.recv(1024).decode())
        if board[move] == " ":
            board[move] = player_symbol
            break
        conn.send(b"INVALID MOVE")

def tic_tac_toe_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12358))
    server_socket.listen(5)
    print("Tic Tac Toe Server is listening...")

    while True:
        conn, addr = server_socket.accept()
        players.put((conn, addr))
        if players.qsize() == 2:
            player1, player2 = players.get(), players.get()
            threading.Thread(target=start_game, args=(player1, player2)).start()

def start_game(player1, player2):
    conn1, addr1 = player1
    conn2, addr2 = player2
    conn1.send(b"Welcome! You're X. Waiting for O.")
    conn2.send(b"Welcome! You're O. X will start.")
    symbols = {"X": conn1, "O": conn2}
    reset_board()

    for i in range(9):
        player_symbol = "X" if i % 2 == 0 else "O"
        conn = symbols[player_symbol]
        handle_player(conn, player_symbol)
        winner = check_winner()
        if winner:
            conn1.send(f"Winner: {winner}".encode())
            conn2.send(f"Winner: {winner}".encode())
            break
    else:
        conn1.send(b"Draw!")
        conn2.send(b"Draw!")

if __name__ == "__main__":
    tic_tac_toe_server()
