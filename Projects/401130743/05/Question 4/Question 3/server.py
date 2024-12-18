import socket
import threading
import logging

# پیکربندی لاگ‌ها
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(conn, addr):
    logging.info(f"کلاینت متصل شد: {addr}")
    try:
        data = conn.recv(1024)
        numbers = eval(data.decode('utf-8'))
        sorted_numbers = sorted(numbers)
        conn.sendall(str(sorted_numbers).encode('utf-8'))
    except Exception as e:
        logging.error(f"خطایی رخ داد: {e}")
    finally:
        conn.close()

def main():
    server_address = ('localhost', 10000)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(server_address)
        s.listen(3)  # منتظر 3 اتصال همزمان
        logging.info('در حال انتظار برای اتصال کلاینت‌ها...')
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except Exception as e:
        logging.error(f"خطای سرور: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    main()