import socket
import threading
import logging

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050

results = {}

# log settings
logging.basicConfig(filename="server.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def handle_so(CONNECTION, so_id):
    try:
        data = CONNECTION.recv(1024).decode()
        print(f"Received sorted array from {so_id}: {data}")
        results[so_id] = data
    except Exception as e:
        logging.error(f"Error in {so_id}: {e}")
    CONNECTION.close()


def main_server():
    global results
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
        print("Server is listening...")
        while True:
            results = {}
            CONNECTION, ADDR = server.accept()
            print(f"Client connected from {ADDR}")
            data = CONNECTION.recv(1024).decode()
            temp_data = []
            for num in data[1:-1].split(','):
                temp_data.append(int(num))
            data = temp_data

            print(f"Received array from client: {data}")

            SO_PORTS = [5051, 5052, 5053]
            idx = 0
            for port in SO_PORTS:
                so_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                so_socket.connect((HOST, port))
                so_socket.send(str(data).encode())
                threading.Thread(target=handle_so, args=(so_socket, f"SO-{idx+1}")).start()
                idx += 1

            while len(results) < 3:
                pass
            response = "\n".join([f"{key}: {value}" for key, value in results.items()])
            CONNECTION.send(response.encode())
            print("Results sent back to client.")
            CONNECTION.close()
    except Exception as e:
        logging.critical(f"Critical error in server: {e}")


if __name__ == "__main__":
    main_server()
