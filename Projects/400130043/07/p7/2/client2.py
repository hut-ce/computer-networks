import socket

def main():
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = input("enter ip: ") 
    port = 12345
    client_s.connect((host, port))
    
    command = input("enter: ")
    
    client_s.send(command.encode())
    
    output = client_s.recv(4096).decode()
    
    print("output:")
    print(output)
    
    client_socket.close()

if __name__ == "__main__":
    main()
