import socket
from threading import Thread
from caesar import caesar_encode, caesar_decode


block_list = []


def receive_messages(client_socket, name: str):
    # Thread function to continuously receive messages from the server.
    while True:
        try:
            message = client_socket.recv(1024).decode()
            message = caesar_decode(message, 11)
            if not message:
                print("Connection closed by server.")
                break
            message = message.split("`~`")
            if message[1] in block_list:
                continue
            elif message[0] == name:
                print(f"Private-{message[1]}: {message[2]}")
            else:
                print(f"{message[1]}: {message[2]}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def send_messages(client_socket, name):
    # Thread function to continuously send messages to the server.
    while True:
        try:
            message = input()
            if message.lower() == 'quit':
                client_socket.send(f"quit`~`{name}`~`".encode())
                print("Disconnected from server.")
                client_socket.close()
                break
            elif 'block>>' in message:
                message = message.split('>>')
                block_list.append(message[1])
            elif '>>' in message:
                message = message.split('>>')
                message = caesar_encode(f'{message[0]}`~`{name}`~`{message[1]}', 11)
                client_socket.send(message.encode())
            else:
                message = caesar_encode(f'message`~`{name}`~`{message}', 11)
                client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
            break


def client_program():
    # Main client function to connect to the server and start threads.
    server_host = '127.0.0.1'
    server_port = 8070

    name = input("Username: ")

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        print(f"Connected to server at {server_host}:{server_port}")
        print('Type "quit" to exit the chat room')
        print('"destination_username>>message" for unicast message ')
        print('"block>>username" for block user')

        # Send initial hello message
        client_socket.send(caesar_encode(f"hello`~`{name}`~`", 11).encode())

        # Start threads for receiving and sending messages
        receive_thread = Thread(target=receive_messages, args=(client_socket, name))
        send_thread = Thread(target=send_messages, args=(client_socket, name))

        receive_thread.start()
        send_thread.start()

        # Wait for both threads to finish
        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == '__main__':
    client_program()

