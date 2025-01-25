import socket

def tic_tac_toe_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12358))
    print(client_socket.recv(1024).decode())

    while True:
        message = client_socket.recv(1024).decode()
        if message.startswith("BOARD"):
            print(message[6:])
            move = input("Enter your move (0-8): ")
            client_socket.send(move.encode())
        elif "Winner" in message or "Draw" in message:
            print(message)
            break

    client_socket.close()

if __name__ == "__main__":
    tic_tac_toe_client()
