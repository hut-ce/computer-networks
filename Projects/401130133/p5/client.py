import socket
import logging

logging.basicConfig(filename="client.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("127.0.0.1", 5555))
        logging.info("Connected to server.")

        role = input("Enter role (client/SO): ").strip()
        if role == "client":
            arr = input("Enter array (e.g., 3 1 4 1 5): ")
            client.send(f"Array:{arr}".encode())
            logging.info(f"Sent array to server: {arr}")

            while True:
                data = client.recv(1024).decode()
                if data:
                    logging.info(f"Received from server: {data}")
                    print(data)
        elif role == "SO":
            while True:
                data = client.recv(1024).decode()
                if data:
                    logging.info(f"Received from server: {data}")
                    print(data)
        else:
            logging.warning("Invalid role entered.")
            print("Invalid role. Please enter 'client' or 'SO'.")
    except Exception as e:
        logging.error(f"Error in client: {e}")
        print(f"Client error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
