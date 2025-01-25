import socket
import threading
import base64
import os
host='127.0.0.1'
port=5000

def send_message(client):
    while True:
        user_input = input("enter message or (type 'sendpic <path>' to send a picture): ")
        if user_input.startswith('sendpic '):
            filepath = user_input.split(' ')[1]
            if os.path.exists(filepath):
                with open(filepath,'rb') as f:
                    image_data = f.read()
                client.sendall(b'pic:'+base64.b64encode(image_data))
                print(f"{filepath} sent")
            else:
                print("file not found")
        else:
            client.sendall(user_input.encode())
def receive_message(client):
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            if data.startwith(b'pic:'):
                filename = 'received_image.png'
                with open(filename,'wb') as f:
                    f.write(base64.b64decode(data[4:]))
                print("image received")
            else:
                print(data.decode())
        except ConnectionResetError:
            break
def start_client():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))
    print(f"connect to {host}:{port}")
    thread=threading.Thread(target=receive_message,args=(client,), daemon=True).start
    send_message(client)

if __name__=="__main__":
    start_client()