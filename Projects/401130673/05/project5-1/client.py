import socket
import threading
import logging
import time
import random


logging.basicConfig(filename='client.log',level=logging.INFO)

def bubble_so(array):
    n = len(array)
    for i in range(n):
          for j in range(0, n-i-1):
               if array[j] > array[j+1]:
                    array[j],array[j+1] = array[j+1], array[j]
    return array     

def stalin_so(array):
    if not array:
        return[]
    sorted_list = [array[0]]
    for i in range(1,len(array)):
        if array[i] >= sorted_list[-1]:
            sorted_list.append(array[i])
    return sorted_list


def is_sorted(array):
    return all(array[i]<=array[i+1] for i in range(len(array)-1))
def bogo_so(array):
    while not is_sorted(array):
        random.shuffle(array)
    return array
     

def handle_client(arr, algorithm):
    start_time = time.time()
    if algorithm == 'bubble_sort':
        sorted_array = bubble_so(arr)
    elif algorithm == 'stalin_sort':
        sorted_array = stalin_so(arr)
    elif algorithm == 'bogo_sort':
        sorted_array = bogo_so(arr)
    else:
        sorted_array = arr
    end_time = time.time()
    spent_time = end_time - start_time
    
    logging.info(f"Sorted array using {algorithm}")
    return spent_time, sorted_array

def start_client(algorithm):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 5050))
        
        if algorithm == 'sender':
            array = input("Please enter an array of numbers, separated by spaces: ")
            client.send(array.encode('utf-8'))
            logging.info(f"Sent array: {array}")
        else:
            data = client.recv(1024).decode('utf-8')
            array = list(map(int, data.split()))
            logging.info(f"Received array: {array}")
            spent_time, sorted_array = handle_client(array, algorithm)
            sorted_array_str = ' '.join(map(str, sorted_array))
            client.send(f'{algorithm},{spent_time},{sorted_array_str}'.encode('utf-8'))
        
        client.close()
    except Exception as e:
        logging.error(f"Client error: {e}")

def main():
    algorithms = ['bubble_sort', 'stalin_sort', 'bogo_sort']
    threads = []

    for algorithm in algorithms:
        thread = threading.Thread(target=start_client, args=(algorithm,))
        threads.append(thread)
        thread.start()

    start_client('sender')

    for thread in threads:
        thread.join()
        
if __name__ == '__main__':
   main()
