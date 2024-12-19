import socket
import threading

def receive_msg():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "USERNAME":
                client.send(username.encode("utf-8"))
            else:
                print(mesage)
        except:
            print("Error")
            client.close()
            break

def send_msg():
    while True:
        user_input = input("")
        message = f"{username}: {user_input}"
        client.send(message.encode("utf-8"))

# اتصال به سرور
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.conect(("127.0.0.1", 5050))

username = input("Enter your username: ")
recv_thread = threading.Thread(target=receive_msg)
recv_thread.start()

send_thread = threading.Thread(target=send_msg)
send_thread.start()
