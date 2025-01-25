import socket
import threading


k_v_store = {}


def handle_client(client_socket):

    while True:
        try:

            data = client_socket.recv(1024).decode()
            if not data:
                break

            
            comnd = data.split(" ")[0]

            if comnd == "SET":

                key = data.split(" ")[1]
                value = " ".join(data.split(" ")[2:])
                k_v_store[key] = value
                client_socket.send(f"OK: Key '{key}' set to '{value}'".encode())
            
            elif comnd == "GET":

                key = data.split(" ")[1]
                if key in k_v_store:
                    client_socket.send(f"Value: {k_v_store[key]}".encode())
                else:
                    client_socket.send(f"Error: Key '{key}' not found".encode())
            
            elif comnd == "DELETE":

                key = data.split(" ")[1]
                if key in k_v_store:

                    del k_v_store[key]
                    client_socket.send(f"OK: Key '{key}' deleted".encode())
                else:
                    client_socket.send(f"Error: Key '{key}' not found".encode())
            
            else:
                client_socket.send("Error: Unknown command".encode())

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    client_socket.close()


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("Server listening on port 8080")

    while True:
        
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
