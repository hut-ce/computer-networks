import socket
import threading
import logging

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(client_socket, address):
    logging.info(f"Connected to: {address}")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            array = list(map(int, data.split(',')))
            logging.info(f"Received array from {address}: {array}")
            
            sorted_array = sorted(array)
            logging.info(f"Sorted array for {address}: {sorted_array}")

            client_socket.send(','.join(map(str, sorted_array)).encode('utf-8'))
    except Exception as e:
        logging.error(f"Error with {address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Connection closed for: {address}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(('0.0.0.0', 12345))
    server.listen(3)
    logging.info("Server started and listening on port 12345")
except Exception as e:
    logging.critical(f"Failed to start server: {e}")
    exit(1)

while True:
    try:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()
    except Exception as e:
        logging.error(f"Error accepting new connection: {e}")
