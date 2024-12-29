import socket
import threading
import pickle
import logging

logging.basicConfig(filename='server_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def sort_array(data, conn):
    try:
        data.sort()
        logging.info(f"Array sorted successfully: {data}")
        conn.send(pickle.dumps(data))
    except Exception as e:
        logging.error(f"Error occurred while sorting data: {e}")
        conn.send(pickle.dumps("Error occurred while processing your request."))  # ارسال پیام خطا به کلاینت
    finally:
        conn.close()


def handle_client(conn, addr):
    try:
        logging.info(f"Connection from {addr} has been established.")

        data = pickle.loads(conn.recv(1024))
        if data:
            sort_array(data, conn)
        else:
            logging.warning(f"No data received from {addr}")
            conn.send(pickle.dumps("No data received."))
    except Exception as e:
        logging.error(f"Error occurred while handling client {addr}: {e}")
        conn.send(pickle.dumps("Error occurred while processing your request."))
        conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))

server.listen(3)
logging.info("Server is listening for connections...")

while True:
    try:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
    except Exception as e:
        logging.error(f"Error accepting client connection: {e}")
