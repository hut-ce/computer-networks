import socket
import threading


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 55555))
    server_socket.listen()
    print(f'[LISTENING] server is listening on {port}')
    while True:
        client_socket, addr = server_socket.accept()
        print(f"{client_socket} is connected to the server!")
        client_socket.close()


threads = []
ports_need_check = [8001, 8005, 8008]

for port in ports_need_check:
    thread = threading.Thread(target=start_server, args=(port,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
