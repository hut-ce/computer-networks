import socket
import threading
import logging
logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                logging.warning("Received empty data from client.")
                break
            
            numbers = list(map(int, data.split()))
            sorted_numbers = sorted(numbers)
            client_socket.send(' '.join(map(str, sorted_numbers)).encode())
        except ValueError as ve:
            logging.error(f"ValueError: {ve}")
            client_socket.send(b"Error: Please send a valid array of numbers.")
        except Exception as e:
            logging.error(f"Error: {e}")
            break
    
    client_socket.close()
    logging.info("Client disconnected.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind(('0.0.0.0', 9999))
    server.listen(3)  

    ip_address = socket.gethostbyname(socket.gethostname())
    logging.info(f"Server is listening on {ip_address}:9999...")
    print(f"Server is listening on {ip_address}:9999...")
    
    while True:
        try:
            client_socket, addr = server.accept()
            logging.info(f"Accepted connection from {addr}")
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except Exception as e:
            logging.error(f"Error accepting connection: {e}")

if __name__ == "__main__":
    main()
