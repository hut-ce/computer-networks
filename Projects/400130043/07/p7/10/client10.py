import socket

class TicTacToeClient:
    def init(self, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def run(self):
        while True:
            message = self.client_socket.recv(1024).decode()
            print(message)
            if "Your turn!" in message:
                position = input("Enter your position (0-8): ")
                self.client_socket.send(position.encode())

if __name__ == "__main__":
    client = TicTacToeClient()
    client.run()
