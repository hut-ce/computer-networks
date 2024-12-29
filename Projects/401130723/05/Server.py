import socket 
import threading
import time
import logging

# پیکربندی لاگینگ
logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(client_socket, addr):
    try:
        data = client_socket.recv(1024).decode()
        array = list(map(int, data.split(',')))
        
        # مرتب‌سازی آرایه با استفاده از الگوریتم‌ها
        sorted_array_stalin = stalin_sort(array)
        sorted_array_bogo = bogo_sort(array.copy())
        sorted_array_bubble = bubble_sort(array.copy())
        
        # ارسال نتایج به کلاینت
        client_socket.send(f'Stalin: {sorted_array_stalin}\nBogo: {sorted_array_bogo}\nBubble: {sorted_array_bubble}'.encode())

        logging.info(f'آرایه دریافت شد از {addr}: {array}')
    except Exception as e:
        logging.error(f"خطا: {e}")
    finally:
        client_socket.close()

def handle_client(client_socket, addr):
    try:
        data = client_socket.recv(1024).decode()
        array = list(map(int, data.split(',')))
        
        start_time_stalin = time.time()
        sorted_array_stalin = stalin_sort(array)
        end_time_stalin = time.time()

        start_time_bogo = time.time()
        sorted_array_bogo = bogo_sort(array.copy())
        end_time_bogo = time.time()

        start_time_bubble = time.time()
        sorted_array_bubble = bubble_sort(array.copy())
        end_time_bubble = time.time()

        times = f'Stalin Sort: {end_time_stalin - start_time_stalin} ثانیه\n' \
                f'Bogo Sort: {end_time_bogo - start_time_bogo} ثانیه\n' \
                f'Bubble Sort: {end_time_bubble - start_time_bubble} ثانیه\n'

        client_socket.send(f'زمان اجرای الگوریتم‌ها:\n{times}'.encode())
    except Exception as e:
        print(f"خطا: {e}")
    finally:
        client_socket.close()

def handle_client(client_socket, addr):
    try:
        # دریافت آرایه از کلاینت
        data = client_socket.recv(1024).decode()
        array = list(map(int, data.split(',')))
        
        # مرتب‌سازی آرایه با استفاده از الگوریتم‌ها
        sorted_array_stalin = stalin_sort(array)
        sorted_array_bogo = bogo_sort(array.copy())
        sorted_array_bubble = bubble_sort(array.copy())
        
        # ارسال نتایج به کلاینت
        client_socket.send(f'Stalin: {sorted_array_stalin}\nBogo: {sorted_array_bogo}\nBubble: {sorted_array_bubble}'.encode("utf_8"))
    except Exception as e:
        print(f"خطا: {e}")
    finally:
        client_socket.close()

def stalin_sort(arr):
    result = [arr[0]]
    for num in arr[1:]:
        if num >= result[-1]:
            result.append(num)
    return result

def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr) - 1))

def bogo_sort(arr):
    import random
    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

ip = socket.gethostbyname(socket.gethostname())
port = 5050
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.listen(10)

print ("server is running")

connection ,addr = server.accept()

while True :
   massage = connection . recv(1024) . decode("utf_8")
   client_socket, addr = server.accept()
   client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
   client_handler.start()
   
   print (f"{massage} is recieved from user {connection}")