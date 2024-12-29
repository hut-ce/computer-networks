import socket
import threading
import pickle


def sort_array(data, conn):
    data.sort()
    conn.send(pickle.dumps(data))
    conn.close()


def handle_client(conn, addr):
    print(f"Connection from {addr} has been established.")

    data = pickle.loads(conn.recv(1024))
    sort_array(data, conn)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))

server.listen(3)

while True:
    conn, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
