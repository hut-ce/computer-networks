import pickle
import socket

def client_interaction():
    host = '127.0.0.1'
    port = 1234

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connected to server at 127.0.0.1:1234")

        while True:
            user_command = input("Enter a command to execute (or type 'exit' to disconnect): ")
            if user_command.lower() == 'exit':
                client_socket.send(pickle.dumps('exit'))
                print("Disconnected from the server.")
                break

            client_socket.send(pickle.dumps(user_command))

            server_response = client_socket.recv(10240)  # Increased buffer size for large outputs
            print("Server response:")
            print(pickle.loads(server_response))


if __name__ == '__main__':
    client_interaction()
