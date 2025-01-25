import socket

def send_request(command):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5055))
        client.send(command.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
    except ConnectionResetError: 
        client.close()
    return response

if __name__ == "__main__":
    
    while True:
            command = input("Enter your command start with (SET, GET) and then enter key and value: ")
            if command.lower() == "exit":
                break
            print(send_request(command))    
    