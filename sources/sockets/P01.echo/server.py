import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65000  # The port used by the server
# MSG = bytes("Hello, world", "utf-8")
s = socket.socket()

s.bind((HOST, PORT))

s.listen(2)

while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   c.send(b'Thank you for connecting')
   c.close()                # Close the connection