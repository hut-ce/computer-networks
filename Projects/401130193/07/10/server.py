import socket
import threading
from queue import Queue

current_board = [" "] * 9
player_queue = Queue()

def display_board():
    return "\n".join(["|".join(current_board[i:i+3]) for i in range(0, 9, 3)])

def determine_winner():
    winning_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for pattern in winning_patterns:
        if current_board[pattern[0]] == current_board[pattern[1]] == current_board[pattern[2]] != " ":
            return current_board[pattern[0]]
    return None

def initialize_board():
    global current_board
    current_board = [" "] * 9

def player_handler(connection, player_char):
    while True:
        connection.send(f"GAME_BOARD\n{display_board()}".encode())
        player_choice = int(connection.recv(1024).decode())
        if current_board[player_choice] == " ":
            current_board[player_choice] = player_char
            break
        connection.send(b"INVALID_MOVE")

def handle_player_connections(server_sock):
    while True:
        conn, address = server_sock.accept()
        player_queue.put((conn, address))
        if player_queue.qsize() == 2:
            player1, player2 = player_queue.get(), player_queue.get()
            threading.Thread(target=start_game_session, args=(player1, player2)).start()

def start_game_session(player1, player2):
    conn1, addr1 = player1
    conn2, addr2 = player2
    conn1.send(b"Hello! You're 'X'. Waiting for 'O'.")
    conn2.send(b"Hello! You're 'O'. 'X' will start.")
    players_conn = {"X": conn1, "O": conn2}
    initialize_board()

    for turn in range(9):
        current_player = "X" if turn % 2 == 0 else "O"
        connection = players_conn[current_player]
        player_handler(connection, current_player)
        winner = determine_winner()
        if winner:
            conn1.send(f"Game Over: {winner} wins!".encode())
            conn2.send(f"Game Over: {winner} wins!".encode())
            break
    else:
        conn1.send(b"Game Over: No Winner.")
        conn2.send(b"Game Over: No Winner.")

def game_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('localhost', 12358))
    server_sock.listen(5)
    print("Server is up and running...")
    handle_player_connections(server_sock)

if __name__ == "__main__":
    game_server()
