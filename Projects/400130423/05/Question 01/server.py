import socket
import threading

ip = "127.0.0.5"

port = 5060

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)

print("Server is running...")

clientsList = []
namesList = []
def clientHandler(connection, address):
    print(f"{connection} is connected to the server.")
    while True:
        #The client handling part of the code
        try:
            message = connection.recv(1024).decode()
            if not message:
                break
            elif message.find("ClientName")+1:
                name = message.split(" ")
                index = clientsList.index(connection)
                namesList[index] = name[1]
            print(f"{namesList[clientsList.index(connection)]} said: {message} \n")
            message = f"\n{namesList[clientsList.index(connection)]} said: {message} \nEnter your message: "
            for client in clientsList:
                if client != connection:
                    client.send(message.encode())
                    
        except ConnectionResetError:
            print(f"Connection with {address} is closed!")
            break
        
    index = clientsList.index(connection)
    clientsList.remove(connection)
    value = namesList[index]
    namesList.remove(value)
    connection.close()
    print(f"{address}:{value} has left the chatroom.")

try:
    while True:
        connection, address = server.accept()
        clientsList.append(connection)
        namesList.append("")
        thread = threading.Thread(target=clientHandler,args=(connection,address))
        thread.start()

except KeyboardInterrupt:
    print("Keyboard interupt. The server is shutting down...")
    server.close()