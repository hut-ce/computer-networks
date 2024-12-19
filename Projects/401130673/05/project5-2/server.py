import socket
import threading
import random
import logging
  
logging.basicConfig(filename='server.log',level=logging.INFO)

def handle_client(client,address,id):
    try:
        print(f"new connection {address} connected!")
        array = client.recv(1024).decode('utf-8').split()
        array =list(map(int,array))
        sorted_arrays = []
        for sorting_algorithm in [stalin_so,bogo_so,bubble_so]:
            sorted_array = sorting_algorithm(array.copy())
            sorted_arrays.append((str(sorting_algorithm).split()[1],sorted_array))

        results = '\n'.join(' '.join(map(str,arr)) for arr in sorted_arrays)
        client.send(results.encode('utf-8'))
        logging.info(f"client {id} sorted array sent successfully!")

    except Exception as exc:
        error_message = f"client {id}: error - {exc}"
        client.send(error_message.encode('utf-8'))
        logging.error(error_message)

    finally:
        client.close()


def is_sorted(array):
    return all(array[i]<=array[i+1] for i in range(len(array)-1))
def bogo_so(array):
    while not is_sorted(array):
        random.shuffle(array)
    return array
     

def stalin_so(array):
    if not array:
        return[]
    sorted_list = [array[0]]
    for i in range(1,len(array)):
        if array[i] >= sorted_list[-1]:
            sorted_list.append(array[i])
    return sorted_list


def bubble_so(array):
    n = len(array)
    for i in range(n):
          for j in range(0, n-i-1):
               if array[j] > array[j+1]:
                    array[j],array[j+1] = array[j+1], array[j]
    return array     


def start(server,id):
     server.listen(4)
     print(f"[listening] server is listening on {server}")
     while True:
        client,address = server.accept()
        id += 1
        logging.info(f"connection from client {id}")
        thread = threading.Thread(target=handle_client,args=(client,address,id))
        thread.start()
        print(f"[active connections] {threading.active_count()-1}")


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    id = 0
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    print("[starting] server is listening...")
    start(server,id)
   

if __name__ == "__main__":
    main()