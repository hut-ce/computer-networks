import socket
import logging

# log settings
logging.basicConfig(filename="client.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((HOST, PORT))

            array = list(map(int, input("Enter an array of numbers separated by spaces: ").strip().split()))
            client.send(str(array).encode())

            data = client.recv(1024).decode()
            print("Sorted results from different SOs:")
            print(data)

            client.close()
        except Exception as e:
            logging.error(f"Error in client: {e}")


if __name__ == "__main__":
    main()
