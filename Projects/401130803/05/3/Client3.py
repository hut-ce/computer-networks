import socket


def main():
    
    IP = socket.gethostbyname(socket.gethostname())
    Port = 5050

    Client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    Client.connect((IP , Port))

    while True:

       
        arr = input("Please Enter an array of Number:\n")
        arr = [int(x) for x in arr.split()]
        Client.send(' '.join(map(str, arr)).encode('utf-8'))
        
        result = Client.recv(1024).decode('utf-8') 
        print(f"sorted array is: {result}")
    

if __name__ == "__main__":
    main()

