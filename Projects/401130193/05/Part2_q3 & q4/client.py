import socket
import logging

# log settings
logging.basicConfig(
    filename="client.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main_client():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    try:
        while True:
            array = input("Enter an array of numbers separated by spaces: ")
            if not array:
                break
            array = list(map(int, array.strip().split()))

            client.send(str(array).encode())

            response = client.recv(1024).decode()
            print(f"Response from server: {response}")
    except Exception as e:
        logging.error(f"error in client (invalid input): {e}")
        client.close()


if __name__ == "__main__":
    main_client()
