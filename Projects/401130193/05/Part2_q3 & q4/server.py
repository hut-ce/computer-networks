import socket
import threading
import logging
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050

# log settings
logging.basicConfig(
    filename="server.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def handle_client(CONNECTION, ADDR):
    print(f"CONNECTION from {ADDR}")
    while True:
        try:
            data = CONNECTION.recv(1024).decode()
            if not data:
                break
            print(f"Received array from {ADDR}: {data}")

            arr = list(map(int, data[1:-1].split(',')))
            sorted_arr = sorted(arr)

            response = f"Sorted array: {sorted_arr}"
            CONNECTION.send(response.encode())
        except Exception as e:
            logging.error(f"Error in server: {e}")
            break

    CONNECTION.close()
    print(f"Connection with {ADDR} closed")


def main_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(3)
        print("Server is listening...")
    except Exception as e:
        logging.error(f"Error in server: {e}")

    while True:
        try:
            CONNECTION, ADDR = server.accept()
            thread = threading.Thread(target=handle_client, args=(CONNECTION, ADDR))
            thread.start()
            print(f"Active CONNECTIONs: {threading.active_count() - 1}")
        except Exception as e:
            logging.error(f"Error in server: {e}")


if __name__ == "__main__":
    main_server()
