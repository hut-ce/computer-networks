import socket
import threading

clients = []


def handle_client(CONNECTION , ADDR):
    print(f"Connected to {ADDR}")
    while True:
        Message = CONNECTION.recv(1024).decode('utf-8')
        if not Message:
            print(f"Connection with {ADDR} is closed")
            break
        #print(f"{Message} is received from {ADDR}")
        broadcast(Message, CONNECTION)#ارسال پیام به بقیه کلاینت ها

    clients.remove(CONNECTION)#حذف کلاینت از لیست
    CONNECTION.close()



def broadcast(Message, CONNECTION):

    for client in clients:
        if client != CONNECTION:
            try:
                client.send(Message.encode('utf-8'))#فرستادن پیام به بقیه کلاینت ها به جز کلاینتی که پیامو وارد کرده
            except:
                clients.remove(client)




def main():
    IP = socket.gethostbyname(socket.gethostname())
    Port = 5050

    Server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    Server.bind((IP , Port))
    Server.listen()

    print("Server is Running!")

    while True:
        CONNECTION , ADDR = Server.accept()
        thread = threading.Thread(target=handle_client , args=(CONNECTION , ADDR))
        thread.start()


if __name__ == "__main__":
    main()