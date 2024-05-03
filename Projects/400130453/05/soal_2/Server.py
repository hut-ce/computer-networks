import socket
import threading
import struct
import time

ip = '127.0.0.3'
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))

server.listen(5)

print("Server is Running and waiting for connections...")

client = []

def stalin_sort(array, connection):

    if not array:
        return array
    
    sorted_array = [array[0]]

    for i in range(1, len(array)):

        if array[i] >= sorted_array[-1]:
            sorted_array.append(array[i])

        else:
            removed_element = array[i]
            removed_element_data = struct.pack('!i', removed_element)            
            connection.sendall(removed_element_data)

    # send 0 to the client knows that there is no removed element
    noElement_remained = struct.pack('!i', 0)
    connection.sendall(noElement_remained)

    return sorted_array



def handle_client(connection, address):
    while True: 
        try:
            encoded_hostname = connection.recv(256)

            if not encoded_hostname:
                    print("Received empty data. Closing connection.")
                    connection.close()
                    break
            
            hostname = encoded_hostname.decode('utf-8').strip('\x00')
            print(f"Received hostname from client: {hostname}")

            length_data = connection.recv(4)
            if not length_data:
                break
            
            length = struct.unpack('!I', length_data)[0]
            
            array_data = connection.recv(4 * length)
            
            if array_data:

                array = struct.unpack(f'!{length}i', array_data)
                
                print(f"Received array from client: {array}")
                
                # Sort the array using Stalin Sort
                sorted_array = stalin_sort(array, connection)
                
                print(f"Sorted array using Stalin Sort: {sorted_array}")
                
                time.sleep(1)

                sorted_length = len(sorted_array)
                sorted_length_data = struct.pack('!I', sorted_length)
                
                sorted_array_data = struct.pack(f'!{sorted_length}i', *sorted_array)
                
                # Send the length of the sorted array
                connection.sendall(sorted_length_data)
                
                # Send the sorted array data
                connection.sendall(sorted_array_data)
                 
        except ConnectionResetError: 
            break 
    
    client.remove(connection)
    connection.close()

try: 
    while True: 
        connection, address = server.accept()
        client.append(connection)

        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

except KeyboardInterrupt: 
    print("Shutting down...")
    server.close()