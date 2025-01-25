import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

print("Enter a command (SET <key> <value>, GET <key>, DELETE <key>):")
command = input()
client.send(command.encode())

response = client.recv(1024).decode()
print("Response from server:", response)

client.close()
