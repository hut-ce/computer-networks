import socket
import logging

HOST = '127.0.0.1'
PORT = 12345

# log
logging.basicConfig(filename='client.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        numbers = input("Enter an array of numbers (space-separated): ")
        client.send(numbers.encode())
        logging.info("Sent data to server")
        sorted_numbers = client.recv(1024).decode()
        print(sorted_numbers)
        logging.info("Received data from server")
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
