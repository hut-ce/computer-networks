import socket as S
import threading as T

ip = '127.0.0.5'
port = 5050

CLI = S.socket(S.AF_INET, S.SOCK_STREAM)
CLI.connect((ip, port))
Name = input("__Name: ")
CLI.send(Name.encode("utf-8"))

def RCV_MSG(CLI):
    while True:
        try:
            MSG = CLI.recv(1024).decode("utf-8")
            if not MSG:
                break
            print("\n", MSG)
            
        
        
        except ConnectionResetError:
            print("Lost the Connection.")
            break


Thread = T.Thread(target=RCV_MSG, args=(CLI,))
Thread.start()
try:
    while True:
        MSG = input(f"__{Name}:")
        CLI.send(MSG.encode("utf-8"))
        

except KeyboardInterrupt:
    print(f"Connection for {Name} is closed.")
    CLI.close()