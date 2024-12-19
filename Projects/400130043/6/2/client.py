import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("disconnect.")
            break

def main():
    server_ip = input("enter server IP: ")
    server_port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        print("connected.")

        thread = threading.Thread(target=receive_messages, args=(client_socket,))
        thread.start()

        while True:
            message = input()
            if message.lower() == 'exit':
                client_socket.send('exit'.encode('utf-8'))
                break
            elif message.startswith('/private'):
                client_socket.send(message.encode('utf-8'))
            else:
                client_socket.send(message.encode('utf-8'))

    except Exception as e:
        print(f" error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
