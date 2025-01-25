import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

command = input("Enter command to execute: ")
client.send(command.encode())

output = client.recv(4096).decode()
print("Output from server:")
print(output)

client.close()
