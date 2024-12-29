import socket

def get_user_input():
    user_input = input("enter numbers: ")
    return list(map(int, user_input.split()))


server_address = ('localhost', 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

try:
    numbers = get_user_input()
    s.sendall(str(numbers).encode('utf-8'))

    for _ in range(3):
        data = s.recv(1024)
        print('sorted data: ', data.decode('utf-8'))
finally:
    s.close()
