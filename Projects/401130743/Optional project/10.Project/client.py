import socket


def start_client():
    server_ip = "127.0.0.1"
    server_port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    print("[CONNECTED] Waiting for another player...")

    while True:
        
        data = client_socket.recv(1024).decode()
        if "turn" in data:
            print(data)  
            move = input("Enter your move (row,col): ")
            client_socket.send(move.encode())  
        elif "wins" in data:
            print(data)
            break
        elif "Invalid move" in data:
            print(data)
        elif "Game Over" in data:
            print(data)
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
