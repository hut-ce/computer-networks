import socket
import threading

IP = '127.0.66.1'
PORT = 4066
Stalin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Stalin.bind((IP, PORT))
Stalin.listen()
print("Stalin is watching...")
Soldiers = []

def Soldier_Handler(connection, address):
    data = []
    Soldier_data = connection.recv(1024).decode('utf-8')
    Soldier_data = Soldier_data.split(sep= ", ")
    Soldiers.append(Soldier_data[0])
    if len(Soldier_data) > 1:
        data.append(Soldier_data[1])
        for i in range(2, len(Soldier_data)):
            if int(Soldier_data[i]) >= int(data[len(data) - 1]):
                data.append(Soldier_data[i])
            else:
                for soldier in Soldiers:
                    if soldier == connection:
                        soldier.send((f"{Soldier_data[0]} Comrade, {Soldier_data[i]} has been deleted from the dataset.\n").encode("utf-8"))
                                    
    for soldier in Soldiers:
        if soldier == connection:
            soldier.send(str(data).encode("utf-8"))
    
    data.clear()
    connection.close()
    Soldiers.remove(connection)
    
try:
    while True:
        connection, address = Stalin.accept()
        Soldiers.append(connection)
        threading.Thread(target=Soldier_Handler, args=(connection, address)).start()
except KeyboardInterrupt:
    print("It has been an honor for Stalin...")
    Stalin.close()