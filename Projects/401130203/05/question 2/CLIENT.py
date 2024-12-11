import socket

def client_program():
    host = socket.gethostbyname(socket.gethostname() )
    port = 5050
    client_socket = socket.socket()
    client_socket.connect((host, port))
    try:
        array = list(map(int, input("Enter numbers separated by spaces: ").split()))
        array_data = ','.join(map(str, array))
        client_socket.send(array_data.encode())
        response = client_socket.recv(1024).decode()
        if response.startswith("ERROR"):
            print("Server error:", response)
        else:
            sorted_array, elapsed_time = response.split('|')
            print(f"Sorted array: {sorted_array}")
            print(f"Execution time: {elapsed_time} seconds")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    client_program()
