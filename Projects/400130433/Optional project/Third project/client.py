import socket


def connect_to_server():
    server_ip = 'localhost'  
    server_port = 8080       
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    while True:
        try:
            data = client.recv(1024).decode()
            if data:
                print("Current Exchange Rates:", data)
            else:
                print("Disconnected from server")
                break
        except:
            print("Error receiving data")
            break

    client.close()

if __name__ == "__main__":
    connect_to_server()
