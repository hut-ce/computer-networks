import socket
import ssl
import threading

HOST = input("enter ip : ")
PORT = 12345

def receive_messages(client_socket):
    """دریافت پیام‌ها از سرور"""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"new msg: {message}")
        except Exception as e:
            print(f"error in received msg: {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    ssl_context = ssl.create_default_context()
    secure_socket = ssl_context.wrap_socket(client_socket)

    try:
        secure_socket.connect((HOST, PORT))
        print("connected!")

        threading.Thread(target=receive_messages, args=(secure_socket,), daemon=True).start()

        while True:
            message = input("enter your msg: ")
            secure_socket.send(message.encode())
    
    except Exception as e:
        print(f"error in connection: {e}")
    finally:
        secure_socket.close()

if __name__ == "__main__":
    main()
