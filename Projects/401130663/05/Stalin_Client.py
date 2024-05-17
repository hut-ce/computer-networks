import socket
import threading

IP = '127.0.66.1'
PORT = 4066
Soldier = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Soldier.connect((IP, PORT))
Soldier_Name = input("Put in your name, Soldier: ")


def Stalin_Call(Soldier):
    while True:
        try:
            Message = Soldier.recv(1024).decode("utf-8")
            if not Message:
                break
            print(Message)
        except ConnectionResetError:
            print("Your connection to STALIN is severed.")
            break

threading.Thread(target=Stalin_Call, args=(Soldier,)).start()

try:
    while True:
        Message = input("Send Data(Only numbers. 0 to send):")
        if Message == "0":
            Soldier.send(Soldier_Name.encode("utf-8"))
            break
        Soldier_Name = Soldier_Name + f", {Message}"
        
except KeyboardInterrupt:
    print(f"Stalin does not need your service anymore, {Soldier_Name}.")
    Soldier.close()