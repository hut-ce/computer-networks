import socket
from threading import Thread
import pickle
from caesar import caesar_encode, caesar_decode

blocklist = []


def receive_messages(client_socket, name: str):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Server closed the connection.")
                break
            decoded_message = pickle.loads(data)
            decoded_message = caesar_decode(decoded_message, 7)
            message_parts = decoded_message.split("`~`")

            if len(message_parts) < 3:
                print(f"Invalid message format: {decoded_message}")
                continue

            if message_parts[1] in blocklist:
                continue
            elif message_parts[0] == name:
                print(f"Private message from {message_parts[1]}: {message_parts[2]}")
            else:
                print(f"{message_parts[1]} says: {message_parts[2]}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def send_messages(client_socket, name):
    while True:
        try:
            message = input()
            if message.lower() == 'out':
                client_socket.send(pickle.dumps(f"out`~`{name}`~`"))
                print("Disconnected from server.")
                client_socket.close()
                break
            elif 'block||' in message:
                message = message.split('>>')
                blocklist.append(message[1])
            elif '||' in message:
                message = message.split('||')
                message = caesar_encode(f'{message[0]}`~`{name}`~`{message[1]}', 7)
                client_socket.send(pickle.dumps(message))
            else:
                message = caesar_encode(f'message`~`{name}`~`{message}', 7)
                client_socket.send(pickle.dumps(message))
        except Exception as e:
            print(f"Error sending message: {e}")
            break


def client_program():
    server_host = '127.0.0.1'
    server_port = 8080
    name = input("Enter your username: ")

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        print('Type "out" to exit the chat room')
        print('"ForWhom||message" for unicast message ')
        print('"block||username" to block a user')

        client_socket.send(pickle.dumps(caesar_encode(f"hello`~`{name}`~`", 7)))

        receive_thread = Thread(target=receive_messages, args=(client_socket, name))
        send_thread = Thread(target=send_messages, args=(client_socket, name))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == '__main__':
    client_program()
