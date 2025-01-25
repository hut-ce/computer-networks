import socket

def main():    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 98))
    while True:
        command = input("Enter command (SET <key> <value>, GET <key>, DELETE <key>): ")
        if command.lower() == "exit":
            break
        client.send(command.encode('utf-8'))
        res = client.recv(1024).decode('utf-8')
        print(f"Server: {res}")
    client.close()

if __name__ == "__main__":
    main()
