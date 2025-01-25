import socket
import threading

host = '127.0.0.1'
port = 5000

clients=[]

def broadcast(sender_client,data):
    for client in clients:
        if (client != sender_client):
            client.send(data.encode())

def handle_client(sender_client):
    while True:
        try:
            data=sender_client.recv(1024).decode()
            print(f"{id(sender_client)} : {data}")
            if not data:
                break
            broadcast(sender_client,data)
        except ConnectionResetError:
            break
    print("client is disconnected")
    clients.remove(sender_client)
    sender_client.close

def start_server():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen()
    print(f"server is listening on {host} , {port}")
    while True:
        client,addr = server.accept()
        print("new connection from {addr}")
        clients.append(client)
        thread=threading.Thread(target=handle_client,args=(client,)).start()

if __name__=="__main__":
    start_server()