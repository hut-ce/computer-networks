import socket
import threading

IP = '127.0.66.1'
PORT = 4066
Clients = []
Client_Names = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(5)
print("The server is running.")

def CLient_Handler (connection, address):
    Client_Name = connection.recv(1024).decode("utf-8")
    Client_Names.append(Client_Name)
    print(f"{Client_Name} has entered the room.")
    while True:
        try:
            Message = connection.recv(1024).decode("utf-8")
            if not Message:
                break
            print (f"{Client_Name}: {Message}")
            for Client in Clients:
                if Client != connection:
                    Client.send((f"{Client_Name}: {Message}").encode("utf-8"))
        except ConnectionResetError:
            print(f"We lost {Client_Name}.")
            break
    connection.close()
    Clients.remove(connection)
    Client_Names.remove(Client_Name)
    print(f"Goodbye, {Client_Name}.")

try:
    while True:
        connection, address = server.accept()
        Clients.append(connection)
        threading.Thread(target=CLient_Handler, args=(connection, address)).start()
except KeyboardInterrupt:
    print(f"The server ({IP}) is shutting down...")
    server.close()
    
    