import socket

def resolve_domain(domain):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 53))
    client.send(domain.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    client.close()
    return response

if __name__ == "__main__":
    while True:
        domain = input("Enter name of your site wit '.com' (or 'exit' to quit): ")
        if domain.lower() == "exit":
            break
        print(resolve_domain(domain))
