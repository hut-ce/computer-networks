import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = input("enter server ip: ")
    port = 12345
    client_socket.connect((host, port))
    
    try:
        while True:
            command = input("دستور (SET <key> <value>, GET <key>, DELETE <key> یا EXIT): ")
            if command.strip().upper() == "EXIT":
                break
            
            client_socket.send(command.encode())
            response = client_socket.recv(1024).decode()
            print(response)
    except KeyboardInterrupt:
        print("out.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
