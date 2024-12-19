import socket
def main_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))

    
    array = input("Enter the array to sort (space-separated): ")
    client.send(array.encode())

   
    print(client.recv(4096).decode())
    print(client.recv(4096).decode())
    client.close()
