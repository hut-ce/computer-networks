import socket
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_input():
    user_input = input("enter numbers:  ")
    return list(map(int, user_input.split()))


server_address = ('localhost', 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(server_address)
    numbers = get_user_input()
    s.sendall(str(numbers).encode('utf-8'))

    data = s.recv(1024)
    print('sorted data', data.decode('utf-8'))
except Exception as e:
    logging.error(f"error {e}")
finally:
    s.close()