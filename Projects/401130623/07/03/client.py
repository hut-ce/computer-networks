import socket

def main():      
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12))
    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            if data:
                print("Current Exchange Rates:", data)
            else:
                print("Disconnected")
                break
        except:
            print("Error receiving")
            break
    client.close()


if __name__ == "__main__":
    main()
