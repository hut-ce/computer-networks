import socket
import threading
import struct
import platform

ip = "127.0.0.3"
port = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((ip, port))

array = []

def send_array(client):
    while True: 
        try: 
            while True:
            
                integer = int(input("Enter an integer (enter 0 to send the array to the server): "))

                if integer == 0:
                    break

                array.append(integer)

            data = struct.pack('!I', len(array))
            data += struct.pack(f'!{len(array)}i', *array)
            
            # Get the hostname
            hostname = platform.node()   

            encoded_hostname = hostname.encode('utf-8')
            encoded_hostname += b'\x00' * (256 - len(encoded_hostname))  # Padding to 256 bytes

            client.sendall(encoded_hostname)
            client.sendall(data)

            print(f"Sent array to server: {array}")
            array.clear()

            print("Receiving removed elements from server:")
            while True:
                try:
                    removed_element_data = client.recv(4)
                    
                    if not removed_element_data:
                        break

                    removed_element = struct.unpack('!i', removed_element_data)[0]

                    if removed_element == 0:
                        break
                
                    print(f"Removed element: {removed_element}")
                except removed_element == 0:
                    break

            length_data = client.recv(4)
            if length_data:
                sorted_length = struct.unpack('!I', length_data)[0]
            
            # Receive the sorted array data
            sorted_array_data = client.recv(4 * sorted_length)

            sorted_array = struct.unpack(f'!{sorted_length}i', sorted_array_data)

            print(f"Received sorted array from server: {sorted_array}")

        except ConnectionResetError and KeyboardInterrupt:
            print("Connection with server is lost!")
            break

try:
    thread = threading.Thread(target=send_array, args=(client,))
    thread.start()
except KeyboardInterrupt:
    print("Connection is getting closed. ")
    client.close()