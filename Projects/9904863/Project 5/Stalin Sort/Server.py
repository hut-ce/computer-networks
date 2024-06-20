import pickle
import socket
import threading

ip="127.0.0.2"
port=5050
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ip,port))
client.send(ip.encode('utf-8'))
print("Now You Can Type A Number To Be Sorted In The List: ")
max_val=0
while True:
    message=input()
    client.send(message.encode('utf-8'))
    
    if int(message) == 0:
        data=client.recv(1024)
        sorted_array=pickle.loads(data)
        print("sorted array is : ",sorted_array)

    if int(message) > max_val:
        max_val=int(message)
    elif int(message) == 0:
        print("connection is closing...")
        client.close()
        break
    else:
        output = client.recv(1024).decode("utf-8")
        print(output)
    