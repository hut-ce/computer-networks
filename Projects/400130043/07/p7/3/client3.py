import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = input("enter ip: ")
    port = 12345
    client_socket.connect((host, port))
    
    try:
        while True:
            message = client_socket.recv(1024).decode()
            print(message)
    except KeyboardInterrupt:
        print("out.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
