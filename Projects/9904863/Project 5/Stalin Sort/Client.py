import pickle
import socket
import threading

ip="127.0.0.2"
port=5050
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
print("Server Is Running And Ready For Clients!")
nums=[]

def removed_num(num):
    connection.send(num.encode('utf-8'))


def stalin_sort(arr):
    result = []
    max_val = float('-inf')
    for num in arr:
        if num >= max_val:
            max_val = num
            result.append(num)
    return result

def client_handler(connection,address):
    print(f"{address} this user is connected!")
    hostname=connection.recv(1024).decode('utf-8')
    while True:
        try:
            num=connection.recv(1024).decode('utf-8')
            if int(num)== 0:
                number=stalin_sort(nums)
                data=pickle.dumps(number)
                print(f"hostname : {hostname}")
                print("sorted array is : ",number)    
                connection.send(data)
                print(f"{address} is disconnected!")
                connection.close
                break
            nums.append(int(num))
            soretd_num=stalin_sort(nums)
            if soretd_num!=nums:
                rnum=int(num)
                nums.remove(rnum)
                message=f"{rnum} has been removed from the list"
                connection.send(message.encode('utf-8'))
            #stalin_sort(nums)  
            
            
        
        except:
            break
    

            

try:
    while True:
        connection,address=server.accept()
        client_handler(connection,address)
except ConnectionResetError:
    connection.close()

