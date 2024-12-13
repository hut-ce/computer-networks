import socket
import threading
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

server.listen(10)


print("Server is Running and is waiting for connections...")

clients = []
exe_times = {}
sorting_algorithms = {1: "stalin sort" ,
                      2: "bogo sort" ,
                      3: "bubble_sort"
                      }


def show_best_time():
    for i in exe_times.keys():
        print(f"{sorting_algorithms[i]} took {exe_times[i]}")


def handle_clients(connection, address):
    print(f"{address} is connected to the server!")
    sorting = False
    while True:
        try:
            command = connection.recv(1024).decode()
            if not command:
                break
            if command == "sort":
                sorting = True
            elif command == "answer":
                sorting = False
            message = connection.recv(1024).decode()

            if not message:
                break
            if sorting:
                print(f"\n<{address}> gave this array to sort: [{message}]")
                print(f"forwarding the array to be sorted to other clients...\n")
                array = message.split(",")

                for i in range(len(clients)):
                    if clients[i] != connection:
                        if not i > 2:
                            # clients[i].send(str(i+1).encode('utf-8'))
                            clients[i].send(f"answer {str(i+1)}".encode('utf-8'))
                        else:
                            clients[i].send("answer 3".encode('utf-8'))
                            # clients[i].send("3".encode('utf-8'))
                        start_time = time.time()
                        clients[i].send(message.encode('utf-8'))
                        end_time = time.time()
                        exe_time = end_time - start_time
                        exe_times[i + 1] = exe_time

                sorting = False
            else:
                connection.send("confirmation 0".encode('utf-8'))
                connection.send(message.encode('utf-8'))
                print(f"    .the sorted array that <{address}> returned is [{message}] forwarding the answer to the client\n")

        except KeyboardInterrupt:
            print(f"Connection with {address} is closed")
            show_best_time()
            break
        except ConnectionResetError:
            print(f"Connection with {address} was forcibly closed")
            break
        finally:
            show_best_time()

    clients.remove(connection)
    connection.close()
    print(f"{address} has left the Sorting System")


try:
    while True:
        connection, address = server.accept()
        clients.append(connection)
        thread = threading.Thread(target=handle_clients, args=(connection, address))
        thread.start()
except KeyboardInterrupt:
    print("Shutting down...")
    show_best_time()
    server.close()
