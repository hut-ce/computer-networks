import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

print("Connected to server.")
while True:
    data = input("Enter a list of numbers separated by commas (or type 'exit' to quit): ")
    if data.lower() == 'exit':
        break

    client.send(data.encode('utf-8'))
    
    sorted_data = client.recv(1024).decode('utf-8')
    print(f"Sorted array from server: {sorted_data}")

client.close()