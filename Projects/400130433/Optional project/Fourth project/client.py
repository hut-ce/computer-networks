import socket


def connect_to_server():
    server_ip = 'localhost'  
    server_port = 8080       
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    while True:
        
        command = input("Enter command (SET <key> <value>, GET <key>, DELETE <key>): ")
        if command.lower() == "exit":
            break
        
        
        client.send(command.encode())

        
        response = client.recv(1024).decode()
        print(f"Server Response: {response}")
    
    client.close()

if __name__ == "__main__":
    connect_to_server()
