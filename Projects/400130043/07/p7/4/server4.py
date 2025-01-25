import socket
import threading

data_store = {}

def handle_client(client_socket):
    """مدیریت ارتباط با کلاینت"""
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break
            
            command, *args = request.split()
            response = ""

            if command == "SET" and len(args) == 2:
                key, value = args
                data_store[key] = value
                response = f"'{key}'  '{value}' saved."
            elif command == "GET" and len(args) == 1:
                key = args[0]
                value = data_store.get(key, "این کلید وجود ندارد.")
                response = f"مقدار کلید '{key}': {value}"
            elif command == "DELETE" and len(args) == 1:
                key = args[0]
                if key in data_store:
                    del data_store[key]
                    response = f" '{key}' deleted."
                else:
                    response = "کليد وجود ندارد."
            else:
                response = "دستور نامعتبر."

            client_socket.send(response.encode())
        except Exception as e:
            print(f"error: {e}")
            break

    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())  
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"server {host}:{port} listening..")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"new connected {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
