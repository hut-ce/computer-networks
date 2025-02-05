import socket

def play_game():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 13000))
    
    print(client.recv(1024).decode())
    while True:
        move = input("Enter your move (0-8): ")
        client.send(move.encode())
        print(client.recv(1024).decode())

if __name__ == "__main__":
    play_game()
