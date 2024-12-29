import socket
import pickle
import logging

logging.basicConfig(filename='client_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_data(data):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5555))
        logging.info(f"Connected to server, sending data: {data}")

        client.send(pickle.dumps(data))
        response = client.recv(1024)
        sorted_data = pickle.loads(response)

        if isinstance(sorted_data, list):
            logging.info(f"Received sorted array: {sorted_data}")
            print("Sorted array:", sorted_data)
        else:
            logging.error(f"Error message from server: {sorted_data}")
            print("Error: ", sorted_data)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print("An error occurred. Check the logs for more details.")
    finally:
        client.close()


# data = list(map(int, input().split()))
data = [5, 4, 6, 2, 1]
send_data(data)
