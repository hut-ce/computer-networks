import socket

def get_prices():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5050))
    client.send("GET PRICES".encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    client.close()
    return response

if __name__ == "__main__":
    while True:
        command = input("Enter 'prices' to get the latest exchange rates or 'exit' to quit: ")
        if command.lower() == "exit":
            break
        elif command.lower() == "prices":
            print(get_prices())
