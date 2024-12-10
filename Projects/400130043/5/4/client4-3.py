import socket
import logging

logging.basicConfig(filename='client.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_ip = input("Enter the server IP address: ")
    
    try:
        client.connect((server_ip, 9999))
        logging.info(f"Connected to server at {server_ip}:9999")
        
        user_input = input("Enter an array of numbers separated by spaces: ")
        client.send(user_input.encode())

        response = client.recv(4096).decode()
        print(f"Sorted results from server: {response}")
        logging.info(f"Received response from server: {response}")

    except ConnectionRefusedError:
        logging.error("Connection refused. Is the server running?")
        print("Connection refused. Is the server running?")
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"An error occurred: {e}")
    finally:
        client.close()
        logging.info("Client disconnected.")

if __name__ == "__main__":
    main()
