import socket
import threading
dic = {}

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            command = data.split(" ")[0]
            if command == "SET":
                key = data.split(" ")[1]
                value = " ".join(data.split(" ")[2:])
                dic[key] = value
                client_socket.send(f"OK: Key '{key}' set to '{value}'".encode('utf-8'))
            elif command == "GET":
                key = data.split(" ")[1]
                if key in dic:
                    client_socket.send(f"Value: {dic[key]}".encode('utf-8'))
                else:
                    client_socket.send(f"Error: Key '{key}' not found".encode('utf-8'))
            elif command == "DELETE":
                key = data.split(" ")[1]
                if key in dic:
                    del dic[key]
                    client_socket.send(f"OK: Key '{key}' deleted".encode('utf-8'))
                else:
                    client_socket.send(f"Error: Key '{key}' not found".encode('utf-8'))
            else:
                client_socket.send("Unknown command".encode('utf-8'))

        except Exception as error:
            print(f"Error handling client: {error}")
            break

    client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 98))
    server.listen(5)
    print("Server is listening on 127.0.0.1:98")

    while True:
        client_socket, addr = server.accept()
        print(f"New connection : {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
