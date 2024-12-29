import socket
import threading

cli = []
client_ = {}

def pkh(py, sender_socket):
    for client in cli:
        if client != sender_socket:
            try:
                client.send(py)
            except Exception as e:
                print(f"{e}")
                client.close()
                cli.remove(client)
def private(py, recipient_name):
    for client, name in client_.items():
        if name == recipient_name:
            try:
                client.send(py)
                return True
            except Exception as e:
                print(f" {e}")
                client.close()
                cli.remove(client)
                return False
    return False
def handle_client(client_socket, dfg):
    name = client_socket.recv(1024).decode('utf-8')
    client_[client_socket] = name
    slm = f"{name}"
    print(slm)
    pkh(slm.encode('utf-8'), client_socket)
    while True:
        try:
            py = client_socket.recv(1024)
            if not py:
                break
            hsk = py.decode('utf-8')
            if hsk.startswith("@"):
                recipient_name, private_msg = hsk[1:].split(" ", 1)
                private(f"Private from {name}: {private_msg}".encode('utf-8'), recipient_name)
            else:
                pkh(f"{name}: {hsk}".encode('utf-8'), client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()
    cli.remove(client_socket)
    dlk = f"{name} left."
    print(dlk)
    pkh(dlk.encode('utf-8'), client_socket)
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 10000))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        cli.append(client_socket)
        print(f"Accepted  {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()