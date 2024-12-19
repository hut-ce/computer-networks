import socket

ip = socket.gethostbyname(socket.gethostname())
port = 5050
client = socket.socket(socket.AF_INET , socket.SOCK_STREAM )
client.connect((ip , port))

response = client.recv(1024).decode("utf_8")
print(f'نتایج مرتب‌سازی:\n{response}')

while True:
    massage = input ("enter your massage please : ")
    client.send(massage. encode("utf_8")) 