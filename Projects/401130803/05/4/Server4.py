import socket
import threading
import logging



logging.basicConfig(filename='server.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def bubble_sort(arr):
    try:
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    except Exception as e:
        logging.error(f"Error in sorting array: {e}")
        return None


def Handle_client(Connection, ADDR):
    logging.info(f"Connected to {ADDR}")
    try:
        while True:
            arr = Connection.recv(1024).decode('utf-8')
            if not arr:
                logging.info(f"Connection with {ADDR} is closed!")
                break
            logging.info(f"Received data from {ADDR}: {arr}")
            try:
                arr = arr.split()  
                arr = [int(x) for x in arr]  
            except ValueError as e:
                logging.error(f"Invalid input from {ADDR}: {e}")
                Connection.send("Invalid input. Please enter integers only.".encode('utf-8'))
                continue  
            
            sorted_arr = bubble_sort(arr)
            if sorted_arr is not None:
                Connection.send(str(sorted_arr).encode('utf-8'))
            else:
                logging.error(f"Sorting failed for {ADDR}")
                Connection.send("Error in sorting the array.".encode('utf-8'))

    except Exception as e:
        logging.error(f"Error handling client {ADDR}: {e}")
        Connection.send("Internal server error.".encode('utf-8'))
    finally:
        Connection.close()


def main():
    IP = socket.gethostbyname(socket.gethostname())
    Port = 5050

    try:
        Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Server.bind((IP, Port))
        Server.listen()
        logging.info("SERVER is running")

        while True:
            Connection, ADDR = Server.accept()
            thread = threading.Thread(target=Handle_client, args=(Connection, ADDR))
            thread.start()

    except Exception as e:
        logging.critical(f"Server error: {e}")


if __name__ == "__main__":
    main()
