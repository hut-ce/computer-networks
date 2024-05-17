import socket as S
import threading as T


IP = '127.40.63.1'
PORT = 4063
CLIs = []

SER = S.socket(S.AF_INET, S.SOCK_STREAM)
SER.bind((IP, PORT))
SER.listen()
print("Server of STALIN is Online...")


def CLI_HNDL(CON, ADR):
    
    DAT = []
   
    MSG = CON.recv(1024).decode('utf-8')
    MSG = MSG.split(sep= ", ")
    
    CLIs.append(MSG[0])
   
    if len(MSG) > 1:     
        DAT.append(MSG[1])
        
        for i in range(2, len(MSG)):
        
            if int(MSG[i]) >= int(DAT[len(DAT) - 1]):
                DAT.append(MSG[i])
             
            else:
                CON.send((f"Stalin server deleted {MSG[i]}.\n").encode("utf-8"))
        
        
        CON.send(str(DAT).encode("utf-8"))
    
    
    DAT.clear()
    CON.close()
    CLIs.remove(CON)
    
    
try:
    while True:
        CON, ADR = SER.accept()
        CLIs.append(CON)
        THR = T.Thread(target=CLI_HNDL, args=(CON, ADR))
        THR.start()
        
except KeyboardInterrupt:
    print("Server of STALIN is shutting down...")
    SER.close()
    
    