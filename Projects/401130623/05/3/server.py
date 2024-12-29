import socket
import threading

def handle_client(conn, addr):
    print(f"client connected: {addr}")
    data = conn.recv(1024)
    numbers = eval(data.decode('utf-8'))
    sorted_numbers = sorted(numbers)
    conn.sendall(str(sorted_numbers).encode('utf-8'))
    conn.close()


server_address = ('localhost', 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)
s.listen(3) 

print('waiting for client connection')
while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
