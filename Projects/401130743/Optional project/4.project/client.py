import socket


def connect_to_server():

    ip = 'localhost'  
    port = 8080       
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    while True:
        
        comnd = input("Enter command (SET <key> <value>, GET <key>, DELETE <key>): ")
        if comnd.lower() == "exit":
            break
        
        
        client.send(comnd.encode())

        
        response = client.recv(1024).decode()
        print(f"Server Response: {response}")
    
    client.close()

if __name__ == "__main__":
    connect_to_server()
