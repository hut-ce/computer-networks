import socket
import logging

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
logging.basicConfig(filename='client.log',level=logging.INFO) 

def main():
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((HOST,PORT))

        array = input("entert your array: ")
        client.send(array.encode('utf-8'))

        result = client.recv(1024).decode('utf-8')
        print("sorted arrays from diffrent algorithms:\n",result)
        logging.info(f"connection from client successfully!")
    except Exception as exc:
        logging.error(f"Client error: {exc}")
    finally:
        client.close()

if __name__ == "__main__":
    main()