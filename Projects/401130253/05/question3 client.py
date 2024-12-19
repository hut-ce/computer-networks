import socket


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 12345))  

    
    array = input("Enter an array of numbers separated by commas: ")
    
    
    client_socket.send(array.encode())
    
    
    result = client_socket.recv(1024).decode()
    print(f"Result from server: {result}")
    
    
    client_socket.close()

if __name__ == "__main__":
    client()
