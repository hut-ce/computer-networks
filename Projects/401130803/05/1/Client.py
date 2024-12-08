import socket

IP = socket.gethostbyname(socket.gethostname())
Port = 5050

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect((IP, Port))

while True:
    arrNumber = input("Please Enter an array of numbers:\n")
    Client.send(str(arrNumber).encode('utf-8'))

    sorted_arr = Client.recv(1024).decode('utf-8')
    print(f"Sorted array is: {sorted_arr}")
