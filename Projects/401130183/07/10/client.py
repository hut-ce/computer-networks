import socket

class TicTacToeClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server_ip = host
        self.server_port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

    def receive_message(self):
        return self.client_socket.recv(1024).decode()

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

    def play_game(self):
        print(self.receive_message())
        while True:
            print(self.receive_message())
            move = input("Enter your move (0-8): ")
            self.send_message(move)
            print(self.receive_message())
            if "Game Over" in self.receive_message():
                break
        self.client_socket.close()


if __name__ == '__main__':
    client = TicTacToeClient()
    client.play_game()
