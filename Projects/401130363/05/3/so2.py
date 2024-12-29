import socket
import pickle


def send_data(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    client.send(pickle.dumps(data))
    response = client.recv(1024)
    print("Sorted array:", pickle.loads(response))
    client.close()


# data = list(map(int, input().split()))
data = [54, 8, 7, 12, 69]
send_data(data)
