import socket
import subprocess
from threading import Thread



def start_client():


    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect(("127.0.0.1", 9999))
    print("Connected to the server.")

    while True:
       
        comm = input("Enter command to execute on server (or 'exit' to quit): ")
        clientsock.send(comm.encode())

        if comm.lower() == "exit":
            print("Disconnecting from server.")
            break

        
        result = clientsock.recv(4096).decode()
        print(f"Result:\n{result}")

    clientsock.close()

if __name__ == "__main__":


    select = input("Run as (server/client): ").strip().lower()


    if select == "server":
        start_server()
    elif select == "client":
        start_client()
    else:
        print("Invalid select. Please select 'server' or 'client'.")
