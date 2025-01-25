import socket

def main():    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 113))
    print("Connected to the server.")
    try:
        while True:
            domain_name = input("Enter the domain or exit to quit): ")
            if domain_name.lower() == "exit":
                break
            client_socket.send(domain_name.encode())
            response = client_socket.recv(1024).decode()
            print(f"response: {response}")
    except:
        print("Connection has been lost.")
    finally:
        client_socket.close()
        print("Client disconnected.")

if __name__ == "__main__":
    main()
