import socket
import threading



def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range (0 , n-i-1):
            if arr[j] > arr[j+1]:
                arr[j] , arr[j+1] = arr[j+1] , arr[j]
    return arr





def Handle_client(Connection , ADDR):
    print(f"Connected to {ADDR}")

    while True:
        arr = Connection.recv(1024).decode('utf-8')
        if not arr:
            print(f"Connection with {ADDR} is closed!")
            break
        print(f"{arr} received from {ADDR}")
        arr = arr.split()  
        arr = [int(x) for x in arr]
        sorted_arr = bubble_sort(arr)
        Connection.send(str(sorted_arr).encode('utf-8'))

    Connection.close()


def main():

    result = []
    IP = socket.gethostbyname(socket.gethostname())
    Port = 5050

    Server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    Server.bind((IP , Port))
    Server.listen()
    print("SERVER is running")

    while True:
        Connection , ADDR = Server.accept()
        thread  = threading.Thread(target=Handle_client , args=(Connection , ADDR))
        thread.start()

if __name__ == "__main__":
    main()