import socket
import logging

logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))
    logging.info("Connected to server.")
    print("Connected to server.")
    
    while True:
        data = input("Enter a list of numbers separated by commas (or type 'exit' to quit): ")
        if data.lower() == 'exit':
            logging.info("Client requested to exit.")
            break
        
        try:
            client.send(data.encode('utf-8'))
            logging.info(f"Sent data to server: {data}")

            sorted_data = client.recv(1024).decode('utf-8')
            print(f"Sorted array from server: {sorted_data}")
            logging.info(f"Received sorted data from server: {sorted_data}")
        except Exception as e:
            logging.error(f"Error during data transmission: {e}")
            print("An error occurred. Check the log for details.")
except Exception as e:
    logging.critical(f"Failed to connect to server: {e}")
    print("Could not connect to the server. Check the log for details.")
finally:
    client.close()
    logging.info("Connection closed.")
