import socket
import threading
import queue

class TicTacToeServer:
    def init(self, host='0.0.0.0', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.queue = queue.Queue()
        print("Server started. Waiting for players...")

    def handle_client(self, client_socket, player_id):
        client_socket.send(f"Welcome {player_id}! Waiting for another player...".encode())
        self.queue.put(client_socket)

        while True:
            if self.queue.qsize() >= 2:
                player1 = self.queue.get()
                player2 = self.queue.get()
                self.start_game(player1, player2)

    def start_game(self, player1, player2):
        board = [' ' for _ in range(9)]
        current_player = player1
        player_symbols = {player1: 'X', player2: 'O'}

        while True:
            self.send_board(player1, board)
            self.send_board(player2, board)

            current_player.send("Your turn! Enter a position (0-8): ".encode())
            position = int(current_player.recv(1024).decode())

            if board[position] == ' ':
                board[position] = player_symbols[current_player]
                if self.check_winner(board):
                    self.send_board(player1, board)
                    self.send_board(player2, board)
                    current_player.send("You win!".encode())
                    (player1 if current_player == player1 else player2).send("You lose!".encode())
                    break
                elif ' ' not in board:
                    self.send_board(player1, board)
                    self.send_board(player2, board)
                    player1.send("It's a draw!".encode())
                    player2.send("It's a draw!".encode())
                    break
                current_player = player2 if current_player == player1 else player1
            else:
                current_player.send("Invalid move! Try again.".encode())

    def send_board(self, client_socket, board):
        board_display = f"{board[0]} | {board[1]} | {board[2]}\n"
        board_display += "---------\n"
        board_display += f"{board[3]} | {board[4]} | {board[5]}\n"
        board_display += "---------\n"
        board_display += f"{board[6]} | {board[7]} | {board[8]}\n"
        client_socket.send(board_display.encode())

    def check_winner(self, board):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]               
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
                return True
        return False

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Player connected from {addr}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, len(self.clients))).start()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.run()
