import socket

def stalins_sort(arr):
    sorted_arr = [arr[0]]
    deleted_numbers = []
    for num in arr[1:]:
        if num >= sorted_arr[-1]:
            sorted_arr.append(num)
        else:
            deleted_numbers.append(num)
    return sorted_arr, deleted_numbers

flag = True
HOST = '127.0.0.5'  
PORT = 5050  

while flag:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Server is listening...")

    conn, addr = server.accept()
    with conn:
        client_hostname = socket.gethostname()
        print('Connected by', client_hostname)
        data = b''
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk
            if b'0' in chunk:
                break
        numbers = data.decode().split()  # Split by spaces
        if '0' in numbers:
            numbers.remove('0')
        else:
            print("No '0' found in the list.")
        
        print("Received numbers:", numbers)
        
        sorted_numbers, deleted_numbers = stalins_sort([int(num) for num in numbers])
        print("Sorted numbers:", sorted_numbers)
        print("Deleted numbers:", deleted_numbers)

        removed_elements_str = ' '.join(map(str, deleted_numbers))
        conn.sendall(removed_elements_str.encode())
        sorted_str = ' '.join(map(str, sorted_numbers))
        conn.sendall(sorted_str.encode())

    server.close()  # Close the server socket
