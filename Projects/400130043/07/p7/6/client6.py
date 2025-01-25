import socket
import time

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = input("enter ip: ")
    port = 12345
    
    for i in range(15):  
        try:
            client_socket.connect((host, port))
            print(f"request {i+1} send.")
            time.sleep(0.1) 
        except Exception as e:
            print(f"error in connection: {e}")
            break
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
