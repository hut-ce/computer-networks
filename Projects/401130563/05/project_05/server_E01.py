import socket
import threading
import random
import time

main_client_connected = False
sorting_functions = ['stalin', 'bubble']  # 'bogo' deleted
UNSORTED_MSG = ''
MAIN_CLIENT_CONNECTION = ''
START_TIME = 0
END_TIME = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5050))
server.listen(4)

print("[LISTENING] server is listening...")


def sending_sorted_arr():
    pass


def received_sorted_arr(conn):
    global START_TIME, END_TIME
    sorted_msg = conn.recv(1024).decode('utf-8')
    END_TIME = time.time()
    elapsed_time = END_TIME - START_TIME
    sorted_msg_with_time = '  time:'.join([sorted_msg, str(elapsed_time)])
    MAIN_CLIENT_CONNECTION.send(sorted_msg_with_time.encode('utf-8'))


def send_message_to_sort(conn, unsorted_mag):
    global START_TIME
    print("[SENDING MESSAGE] sending unsorted message to oder three clients")
    selected_function = random.choice(sorting_functions)
    sorting_functions.remove(selected_function)
    unsorted_msg_with_sort_func = ':'.join([selected_function, unsorted_mag])
    START_TIME = time.time()
    conn.send(unsorted_msg_with_sort_func.encode('utf-8'))
    received_sorted_arr(conn)


def receiving_unsorted_msg(conn, addr):
    global UNSORTED_MSG
    msg = conn.recv(1024).decode('utf-8')
    UNSORTED_MSG = msg
    print(f"[RECEIVED MESSAGE] {addr}: {msg}")


try:
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} has been connected...")
        if main_client_connected:
            threading.Thread(target=send_message_to_sort, args=(conn, UNSORTED_MSG)).start()
        else:
            receiving_unsorted_msg(conn, addr)
            MAIN_CLIENT_CONNECTION = conn
            main_client_connected = True

except KeyboardInterrupt:
    print(" [SHUTTING] Server is shutting down...")
    server.close()
