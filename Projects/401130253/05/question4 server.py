import socket
import threading
import random
import time


def bubble_sort(arr):
    try:
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    except Exception as e:
        return f"Error during sorting: {str(e)}"


def handle_client(client_socket, client_address):
    try:
        print(f"Connection from {client_address}")
        
        data = client_socket.recv(1024).decode()  
        if not data:
            raise ValueError("No data received.")
        
        
        array = list(map(int, data.split(',')))
        print(f"Received array: {array}")

        
        start_time = time.time()

        
        sorted_array = bubble_sort(array)

        
        end_time = time.time()
        elapsed_time = end_time - start_time  
        
        if isinstance(sorted_array, str):  
            result = f"Error: {sorted_array}"
        else:
            result = f"Sorted Array: {sorted_array} (Time: {elapsed_time:.4f} seconds)"
        
        
        client_socket.send(result.encode())
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(f"Error: {str(e)}")
        client_socket.send(error_message.encode())
    finally:
        
        client_socket.close()


def server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", 12345))
        server_socket.listen(3)  
        
        print("Server is listening for connections...")
        
        
        threads = []
        for _ in range(3):
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            threads.append(thread)
            thread.start()
        
        
        for thread in threads:
            thread.join()
    except Exception as e:
        print(f"Server error: {str(e)}")
    finally:
        
        server_socket.close()

if __name__ == "__main__":
    server()
