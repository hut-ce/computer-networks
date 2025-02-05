import socket
import threading

clients = []
board = [" "]*9

def handle_client(conn, player):
    conn.send(f"Welcome Player {player}".encode())
    while True:
        move = int(conn.recv(1024).decode())
        if board[move] == " ":
            board[move] = "X" if player == 1 else "O"
        conn.send(str(board).encode())

def start_game_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 13000))
    server.listen(2)
    
    for i in range(2):
        conn, addr = server.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, i+1)).start()

if __name__ == "__main__":
    start_game_server()
