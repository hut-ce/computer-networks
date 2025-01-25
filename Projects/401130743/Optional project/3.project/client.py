import socket


def connect_to_server():


    ip = 'localhost'  
    port = 8080       
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

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
