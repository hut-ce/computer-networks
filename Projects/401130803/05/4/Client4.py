import socket
import logging



logging.basicConfig(filename='client.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def receive_full_response(client_socket, buffer_size=1024):
    response = b""
    try:
        while True:
            chunk = client_socket.recv(buffer_size)
            response += chunk
            if len(chunk) < buffer_size:
                break
        return response.decode('utf-8')
    except Exception as e:
        logging.error(f"Error receiving data from server: {e}")
        return None


def main():
    IP = socket.gethostbyname(socket.gethostname())
    Port = 5050

    try:
        Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Client.connect((IP, Port))
        logging.info(f"Connected to server at {IP}:{Port}")

        while True:
            arr = input("Please Enter an array of Numbers (space-separated):\n")
            try:
                arr = [int(x) for x in arr.split()]
            except ValueError:
                logging.error(f"Invalid input from user: {arr}")
                print("Invalid input. Please enter only integers.")
                continue  

            
            Client.send(' '.join(map(str, arr)).encode('utf-8'))
            logging.info(f"Sent data to server: {arr}")

            
            result = receive_full_response(Client)
            if result is not None:
                print(f"Sorted array is: {result}")
            else:
                logging.error("Failed to receive a valid response from server.")
                print("Failed to receive sorted array from server.")
                
    except Exception as e:
        logging.critical(f"Error connecting to server: {e}")
        print("Unable to connect to server. Exiting...")

    finally:
        Client.close()
        logging.info("Client connection closed.")


if __name__ == "__main__":
    main()
