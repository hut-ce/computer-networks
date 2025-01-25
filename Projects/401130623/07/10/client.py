import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 45))
    print("Waiting for player")
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if "turn" in data:
            print(data)  
            move = input("your move [ row , column ] : ")
            client_socket.send(move.encode('utf-8'))  
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
    main()
