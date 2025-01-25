import socket

def currency_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12347))
    print("Connected to Currency Server...")
    try:
        while True:
            print("Requesting latest currency prices...")
            client_socket.send(b"GET_PRICES")
            response = client_socket.recv(1024).decode()
            print(f"Latest Prices:\n{response}")
            input("Press Enter to refresh (or type 'exit' to quit): ")
            if response.lower() == 'exit':
                break
    finally:
        client_socket.send(b"exit")
        client_socket.close()
        print("Disconnected from server.")

if __name__ == "__main__":
    currency_client()
