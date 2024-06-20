import socket
import threading

ip = "127.0.0.5"
port = 50600

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,port))
server.listen()

print("Server is running...")

clientsList = []

def clientHandler(connection, address):
    print(f"{connection} is connected to the server.")
    while True:
        try:
            recievedData = []
            clientData = connection.recv(1024).decode()
            if not clientData:
                break
            clientData = clientData.split(sep= " ")
            name = clientData[0]
            clientsList.append(name)
            if len(clientData) > 1:
                recievedData.append(clientData[1])
                for i in range(2, len(clientData)):
                    if int(clientData[i]) >= int(recievedData[len(recievedData) - 1]):
                        recievedData.append(clientData[i])
                    else:
                        for client in clientsList:
                            if client == connection:
                                client.send((f"{name} : {clientData[i]} was removed.\n").encode("utf-8"))
                                            
            for client in clientsList:
                if client == connection:
                    client.send(str(recievedData).encode("utf-8"))
            
            #recievedData.clear()
        except ConnectionResetError:
            print(f"Connection with {address} is closed!")
            break
    
    recievedData.clear()
    connection.close()
    clientsList.remove(connection)

try:
    while True:
        connection, address = server.accept()
        clientsList.append(connection)
        threading.Thread(target=clientHandler, args=(connection, address)).start()

except KeyboardInterrupt:
    print("Keyboard interupt. The server is shutting down...")
    server.close()