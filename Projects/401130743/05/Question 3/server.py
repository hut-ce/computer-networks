import socket
import threading

def handle_client(conn, addr):
    print(f"کلاینت متصل شد: {addr}")
    data = conn.recv(1024)
    numbers = eval(data.decode('utf-8'))
    sorted_numbers = sorted(numbers)
    conn.sendall(str(sorted_numbers).encode('utf-8'))
    conn.close()

def main():
    server_address = ('localhost', 10000)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(server_address)
    s.listen(3)  # منتظر 3 اتصال همزمان

    print('در حال انتظار برای اتصال کلاینت‌ها...')
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()