import socket
import threading
import queue

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.winner = None

    def display_board(self):
        return f"""
        {self.board[0]} | {self.board[1]} | {self.board[2]}
        ---------
        {self.board[3]} | {self.board[4]} | {self.board[5]}
        ---------
        {self.board[6]} | {self.board[7]} | {self.board[8]}
        """

    def make_move(self, position):
        if self.board[position] == ' ' and self.winner is None:
            self.board[position] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return True
        return False


class Server:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.client_queue = queue.Queue()
        self.lock = threading.Lock()

    def handle_client(self, client_socket, client_address):
        game = TicTacToe()
        client_socket.sendall(b"Welcome to Tic-Tac-Toe! Waiting for another player...")

        with self.lock:
            if self.client_queue.qsize() % 2 == 0:
                self.client_queue.put(client_socket)
                if self.client_queue.qsize() == 2:
                    player1 = self.client_queue.get()
                    player2 = self.client_queue.get()
                    self.start_game(player1, player2, game)
            else:
                self.client_queue.put(client_socket)

    def start_game(self, player1, player2, game):
        player1.sendall(f"Your move, you are 'X'.\n{game.display_board()}".encode())
        player2.sendall(f"Your move, you are 'O'.\n{game.display_board()}".encode())
        while game.winner is None:
            self.play_turn(player1, player2, game)

        if game.winner:
            player1.sendall(f"Game Over! {game.winner} wins!\n{game.display_board()}".encode())
            player2.sendall(f"Game Over! {game.winner} wins!\n{game.display_board()}".encode())
        else:
            player1.sendall(f"Game Over! It's a tie!\n{game.display_board()}".encode())
            player2.sendall(f"Game Over! It's a tie!\n{game.display_board()}".encode())
        player1.close()
        player2.close()

    def play_turn(self, player1, player2, game):
        if game.current_player == 'X':
            player_socket = player1
        else:
            player_socket = player2
        player_socket.sendall(f"Your turn, please select a position (0-8):\n{game.display_board()}".encode())
        move = player_socket.recv(1024).decode().strip()
        try:
            move = int(move)
            if move < 0 or move > 8:
                player_socket.sendall(b"Invalid position. Try again.\n")
                return
            if not game.make_move(move):
                player_socket.sendall(b"Invalid move. Try again.\n")
                return
        except ValueError:
            player_socket.sendall(b"Invalid input. Try again.\n")
            return

    def run(self):
        print("Server is running, waiting for players...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection: {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()


if __name__ == '__main__':
    server = Server()
    server.run()
