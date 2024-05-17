import socket as S
import threading as T

IP = '127.40.63.1'
PORT = 4063
DAT = ""

CLI = S.socket(S.AF_INET, S.SOCK_STREAM)
CLI.connect((IP, PORT))

Name = input("Name: ")
DAT = Name


def RCV_MSG(CLI):
    while True:
        try:
            MSG = CLI.recv(1024).decode("utf-8")
           
            if not MSG:
                break
           
            print(MSG)
            
        except ConnectionResetError:
            print("Out of STALIN'S reach.")
            break


THR = T.Thread(target=RCV_MSG, args=(CLI,))
THR.start()


try:
    while True:
        MSG = input("Give data(0 to send):")
        
        
        if MSG == "0":
            CLI.send(DAT.encode("utf-8"))
            break
        
        
        DAT = DAT + f", {MSG}"
    
except KeyboardInterrupt:
    print(f"{Name}, you are out of STALIN's reach.")
    CLI.close()