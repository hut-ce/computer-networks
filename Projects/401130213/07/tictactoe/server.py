import socket
import threading
import pickle

BOARD = [['-', '-', '-'],['-', '-', '-'],['-', '-', '-']]

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((IP, PORT))

SERVER.listen()

print("Server is Running and is waiting for connections...")

clients = []
playing = []
waiting_queue = []

def evaluate():
    winner = ''
    if BOARD[0][0] == BOARD[0][1] == BOARD[0][2] and BOARD[0][0] != '-':
        winner = BOARD[0][0]
    elif BOARD[0][0] == BOARD[1][1] == BOARD[2][2] and BOARD[0][0] != "-":
        winner = BOARD[0][0]
    elif BOARD[0][0] == BOARD[1][0] == BOARD[2][0] and BOARD[0][0] != "-":
        winner = BOARD[0][0]

    elif BOARD[0][1] == BOARD[1][1] == BOARD[2][1] and BOARD[0][1] != "-":
        winner = BOARD[0][1]

    elif BOARD[0][2] == BOARD[1][2] == BOARD[2][2] and BOARD[0][2] != "-":
        winner = BOARD[0][2]
    elif BOARD[0][2] == BOARD[1][1] == BOARD[2][0] and BOARD[0][2] != "-":
        winner = BOARD[0][2]

    elif BOARD[1][0] == BOARD[1][1] == BOARD[1][2] and BOARD[1][0] != "-":
        winner = BOARD[1][0]
    elif BOARD[2][0] == BOARD[2][1] == BOARD[2][2] and BOARD[2][0] != "-":
        winner = BOARD[2][0]

    if winner:
        if winner == "X":
            return "player1"
        else:
            return "player2"


def draw_board(pos_x, pos_y, player_name):
    if player_name == 'player1':
        player_mark = 'X'
    else:
        player_mark = 'O'
    if BOARD[pos_x][pos_y] == '-':
        BOARD[pos_x][pos_y] = player_mark

    print(BOARD)


def handle_clients(connection, address, player_mark):
    print(f"{address} is connected to the server!")
    winner_flag = False
    while True:
        try:
            message = connection.recv(1024).decode()
            player_name, positions = message.split(":")
            pos_x, pos_y = positions.split(",")
            draw_board(int(pos_x), int(pos_y), player_name)
            winner = evaluate()
            if winner:
                print(f"{winner} won!")
                winner_flag = True

            if not message:
                break
            print(f"{address} said {message}")

            for c in clients:
                if c != connection:
                    if not winner_flag:
                        BOARD_data = pickle.dumps(BOARD)
                        c.send(BOARD_data)
                    else:
                        c.send(b'you lost!')
            if winner_flag:
                connection.send(b'you lost!')
        except KeyboardInterrupt:
            print(f"Connection with {address} is closed")
            break
        except ConnectionResetError:
            print(f"Connection with {address} was forcibly closed")
            break
        except ValueError:
            print(f"something went wrong!")
            break

    clients.remove(connection)
    playing.remove(connection)
    connection.close()
    print(f"{address} has left the chatroom!")


try:
    while True:
        if len(playing) < 2:
            if waiting_queue:
                connection1, address1 = waiting_queue[0]
                waiting_queue.remove((connection1, address1))
                if waiting_queue:
                    connection2, address2 = waiting_queue[0]
                    waiting_queue.remove((connection2, address2))
                else:
                    connection2, address2 = SERVER.accept()
            else:
                connection1, address1 = SERVER.accept()
                connection2, address2 = SERVER.accept()
            clients.append(connection1)
            playing.append(connection1)

            clients.append(connection2)
            playing.append(connection2)

            BOARD = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
            BOARD_data = pickle.dumps(BOARD)
            connection1.send(b'player1' + BOARD_data)

            connection2.send(b'player2' + BOARD_data)

            connection1.send(BOARD_data)
            thread1 = threading.Thread(target=handle_clients, args=(connection1, address1, 'X'))
            thread2 = threading.Thread(target=handle_clients, args=(connection2, address2, 'O'))
            thread1.start()
            thread2.start()

except KeyboardInterrupt:
    print("Shutting down...")
    SERVER.close()


