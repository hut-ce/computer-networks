import socket
import logging

logging.basicConfig(filename='client_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_ip = '127.0.0.1'  
        server_port = 5555
        client_socket.connect((server_ip, server_port))
        logging.info("Connected to the server.")
        
        array = [5, 3, 8, 6, 2, 7]
        array_str = ','.join(map(str, array))
        try:
            client_socket.send(array_str.encode('utf-8'))
            logging.info("Array sent to server.")
        except Exception as e:
            logging.error(f"Error sending data to server: {str(e)}")
            client_socket.close()
            return
        
        try:
            response = client_socket.recv(1024).decode('utf-8')
            logging.info(f"Server response: {response}")
        except Exception as e:
            logging.error(f"Error receiving data from server: {str(e)}")
            client_socket.close()
            return
        
        try:
            sorted_response = client_socket.recv(1024).decode('utf-8')
            logging.info(f"Sorted result from server: {sorted_response}")
        except Exception as e:
            logging.error(f"Error receiving sorted data from server: {str(e)}")
        
    except Exception as e:
        logging.error(f"Error connecting to server: {str(e)}")
    finally:
        client_socket.close()
        logging.info("Connection closed.")

if __name__ == "__main__":
    client_program()