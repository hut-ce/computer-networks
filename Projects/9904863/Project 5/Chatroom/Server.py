import socket
import threading

ip="127.0.0.2"
port=5050
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
print("Server Is Running And Ready For Clients!")
clients=[]


def client_handler(connection,address):
    print(f"{address} this user is connected!")
    name=connection.recv(1024).decode('utf-8')
    clients.append((connection,name))
    while True:
        try:
            message=connection.recv(1024).decode('utf-8')
            
            if not message:
                break
        
            if message.strip().lower() == 'exit' :
                print(f"{connection}:{name} disconnected! ")
                clients.remove((connection,name))
                connection.close()
                break
            
            print(f"{name} said : {message}")
        
        except:
            break
    

            

try:
    while True:
        connection,address=server.accept()
        thread=threading.Thread(target=client_handler, args=(connection,address))
        thread.start()
except ConnectionResetError:
    connection.close()

