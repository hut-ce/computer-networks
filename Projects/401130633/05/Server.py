import socket as S
import threading as T


ip = '127.0.0.5'
port = 5050
CLIs = []
CLINs = []
SER = S.socket(S.AF_INET, S.SOCK_STREAM)
SER.bind((ip, port))
SER.listen(5)
print(f"The server [{ip}] is online...")

def CLI_HNDL (CON, ADR):
    Name = CON.recv(1024).decode("utf-8")
    CLINs.append(Name)
    print(f"Hello and welcome, {Name}!")
    
    while True:
        try:
            MSG = CON.recv(1024).decode("utf-8")
            if not MSG:
                break
            
            
            if MSG == "dive" or MSG == "Dive":
                for CLI in CLIs:
                    if CLI != CON:
                        print (f"__{Name}: {MSG}")
                        print (f"{Name} is diving out.")
                break
            
            
            print (f"{Name}: {MSG}")
            for CLI in CLIs:
                if CLI != CON:
                    CLI.send((f"__{Name}: {MSG}").encode("utf-8"))
            
            
        except ConnectionResetError:
            print(f"We lost {Name}.")
            break
        
    
    
    CON.close()
    CLIs.remove(CON)
    CLINs.remove(Name)
    print(f"Goodbye, {Name}.")


try:
    while True:
        CON, ADR = SER.accept()
        CLIs.append(CON)
        THR = T.Thread(target=CLI_HNDL, args=(CON, ADR))
        THR.start()

       
except KeyboardInterrupt:
    print(f"The server ({ip}) is shutting down...")
    SER.close()
    
    